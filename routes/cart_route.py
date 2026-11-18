from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from connection import get_conn
from models.cart_model import Cart
from models.cart_item_model import Cart_item
from models.product_model import Product

cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/api/cart",
)


@cart_bp.route("", methods=["GET"])
@jwt_required()
def cart():
    user_id = int(get_jwt_identity())

    conn = get_conn()
    cursor = conn.cursor()

    cart = Cart.find_cart(
        cursor,
        user_id,
        is_active=1,
    )
    if not cart:
        return jsonify({"error": "No Cart Found..."}), 404
    return jsonify(cart.convert())


@cart_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
@jwt_required()
def added(product_id):
    user_id = int(get_jwt_identity())

    conn = get_conn()
    cursor = conn.cursor()

    product = Product.find_product(cursor, product_id)
    if not product:
        return jsonify({"error": "product Not Found..."}),404

    if product.in_stock <= 0:
        return jsonify({"error": f"{product.product_name} is Out Of Stock.."}), 400

    cart = Cart.find_cart(cursor, user_id)
    if not cart:
        new_cart = Cart(user_id)
        if new_cart.active_in_active(cursor, conn):

            cart_item = Cart_item(product.product_id, new_cart.cart_id)
            cart_item_created = cart_item.save_update(cursor, conn)
            if cart_item_created:
                return jsonify(
                    cart_item.find_cart_item(
                        cursor, cart_item_id=cart_item.cart_item_id
                    ).convert()
                ),201
            return (
                jsonify({"error": "server related error with saving cart item.."}),
                500,
            )

        return jsonify({"error": "cart creation error...server related"}), 500

    cart_item = Cart_item(
        product_id=product.product_id,
        cart_id=cart.cart_id,
    )
    cart_item_check = cart_item.find_cart_item_cartId_and_product_id(
        cursor,
        cart.cart_id,
        product_id,
    )
    if cart_item_check:
        if cart_item_check.quantity >= product.in_stock:
            return (
                jsonify({"error": "Limited Quantity Reached...."}),
                400,
            )

        cart_item_check.quantity += 1
        cart_item_check.save_update(
            cursor,
            conn,
        )
        return jsonify(
            cart_item.find_cart_item(
                cursor,
                cart_item_check.cart_item_id,
            ).convert()
        ),201

    create_cart_item = cart_item.save_update(
        cursor,
        conn,
    )

    if create_cart_item:
        return (
            jsonify(cart_item.find_cart_item(cursor, cart_item.cart_item_id).convert()),
            201,
        )
    return jsonify({"error": "error creating cart_item..."}), 500


@cart_bp.route("/delete_from_cart/<int:cart_item_id>", methods=["DELETE"])
@jwt_required()
def delete(cart_item_id):
    conn = get_conn()
    cursor = conn.cursor()
    user_id = int(get_jwt_identity())

    user_cart = Cart.find_cart(cursor, user_id)
    if not user_cart:
        return jsonify({"error": "user Has No Active cart"}), 404

    find_cart_item = Cart_item.find_cart_item(
        cursor,
        cart_item_id,
    )
    if not find_cart_item:
        return jsonify({"error": "Cart item Not Found..."}), 404

    if find_cart_item.cart_id != user_cart.cart_id:
        return jsonify({"error": "Ownership Required..."}), 403

    cursor.execute("DELETE FROM cart_items WHERE id = ?", (cart_item_id,))
    conn.commit()
    return jsonify({"success": " cart_item deleted"}), 200


@cart_bp.route("/decrease_delete_cart_item/<int:cart_item_id>", methods=["PUT"])
@jwt_required()
def update(cart_item_id):
    conn = get_conn()
    cursor = conn.cursor()

    user_id = int(get_jwt_identity())

    user_cart = Cart.find_cart(cursor, user_id)
    if not user_cart:
        return jsonify({"error": "user has No Active Cart..."}), 404

    user_cart_items = user_cart.cart_items
    if not user_cart_items:
        return jsonify({"error": "user has no item in Cart"}), 404

    cart_item = Cart_item.find_cart_item(cursor, cart_item_id)
    if not cart_item:
        return jsonify({"error": "Cart_item Not Found..."}), 404

    # if cart_item.convert() not in user_cart_items:
    if cart_item.cart_id != user_cart.cart_id:
        return jsonify({"error": "Ownership required..."}), 403

    cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cursor.execute("DELETE FROM cart_items WHERE id =?", (cart_item.cart_item_id,))
        conn.commit()
        return (
            jsonify({"success": f"{cart_item.product_name} removed successfully"}),
            200,
        )
    cart_item.save_update(cursor, conn)
    return jsonify(cart_item.convert()), 200


@cart_bp.route("/cart_item/<int:cart_item_id>", methods=["GET"])
@jwt_required()
def cart_item(cart_item_id):
    conn = get_conn()
    cursor = conn.cursor()

    cart_item = Cart_item.find_cart_item(cursor, cart_item_id)
    if not cart_item:
        return jsonify({"error": "cart Item Not Found..."}), 404
    user_cart = Cart.find_cart(cursor, user_id=int(get_jwt_identity()))
    if not user_cart:
        return jsonify({"error": "user has No Active Cart..."}), 404
    if cart_item.cart_id != user_cart.cart_id:
        return jsonify({"error": "Ownership Required..."}), 403
    return jsonify(cart_item.convert()), 200
