from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify, Blueprint
from connection import get_conn
from models.cart_model import Cart
from models.product_model import Product
from models.order_model import Order

order_bp = Blueprint(
    "order",
    __name__,
    url_prefix="/api/order",
)


@order_bp.route("/checkout", methods=["POST"])
@jwt_required()
def ordered():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        user_id = int(get_jwt_identity())

        order_cart = Cart.find_cart(cursor, user_id)
        if not order_cart:
            return jsonify({"error": "No Cart Found For Order"}), 404
        order_cart_items = order_cart.cart_items
        if not order_cart_items:
            return jsonify({"error": "No Cart_item Found For Order"}), 404

        for each_item in order_cart_items:
            product_id = each_item.get("product_id")
            quantity = each_item.get("quantity")

            product = Product.find_product(cursor, product_id)
            if not product:
                return jsonify({"error": "product not Found..."}), 404
            if product.in_stock < quantity:
                return (
                    jsonify({"error": f"{product.product_name} is Out of Stock"}),
                    400,
                )
        order = Order(user_id, order_cart.total_price,order_cart_items,status_id=1)
        if order.save_update(conn, cursor):
            for each_item in order_cart_items:
                product = Product.find_product(cursor, each_item.get("product_id"))
                product.in_stock -= each_item.get("quantity")
                product.save_update(conn,cursor)
        

            print("payment loading.....")
            payment_confirmed = True
            if not payment_confirmed:
                return jsonify({"error": "PaYment Transaction Declined..."}), 400
            order.status_id =2
       
            order_cart.is_active =0
            order_cart.active_in_active(cursor,conn)
            return jsonify(order.find_order(cursor, order.order_id).convert()),201
        return jsonify({'error':'failed saving order'}),500
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "unexpected error ", "details": f"{ str(e)}"}), 500
