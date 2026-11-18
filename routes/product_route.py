from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from utils.decorators import admin_required
from connection import get_conn
from models.product_model import Product

product_bp = Blueprint(
    "product",
    __name__,
    url_prefix="/api/products",
)


@product_bp.route("", methods=["POST"])
@admin_required
def create_product():
    conn = get_conn()
    cursor = conn.cursor()

    data = request.get_json()

    product_name = data.get("product_name")
    price = data.get("price")
    in_stock = data.get("in_stock", 0)
    
    if not product_name or not price:
        return jsonify({"error": "Invalid Input"}), 400
    product = Product(
        product_name,
        price,
        in_stock,
    )
    if product.save_update(
        conn,
        cursor,
    ):
        return jsonify(product.find_product(cursor, product.product_id).convert())
    return jsonify({"error": "server Error saving product..."}), 500


@product_bp.route("<int:product_id>", methods=["PUT"])
@admin_required
def update(product_id):
    conn = get_conn()
    cursor = conn.cursor()

    product = Product.find_product(
        cursor,
        product_id,
    )
    if not product:
        return jsonify({"error": "Product Not Found..."}), 404

    data = request.get_json()

    product.product_name = data["product_name"] if data.get("product_name") else product.product_name
    product.price = data["price"] if data.get("price") else product.price
    product.in_stock = data["in_stock"] if data.get("in_stock") else product.in_stock
    if product.save_update(conn, cursor):
        return jsonify(product.convert()), 200
    return jsonify({"error": "server error saving product"}), 500


@product_bp.route("<int:product_id>", methods=["GET"])
def product(product_id):

    conn = get_conn()
    cursor = conn.cursor()

    product = Product.find_product(
        cursor,
        product_id,
    )
    if product:
        return jsonify(product.convert()), 200
    return jsonify({"error": "Product Not Found..."}), 404


@product_bp.route("<int:product_id>", methods=["DELETE"])
@admin_required
def delete(product_id):

    conn = get_conn()
    cursor = conn.cursor()

    product = Product.find_product(
        cursor,
        product_id,
    )
    if product:
        cursor.execute("DELETE FROM products WHERE id =?", (product_id,))
        conn.commit()
        return (
            jsonify(
                {
                    "success": f"product Name:{product.product_name} Deleted successfully..."
                }
            ),
            200,
        )
    return jsonify({"error": "product Not found..."}), 404


@product_bp.route('',methods = ['GET'])
def products ():
    conn = get_conn()
    cursor = conn.cursor()
    
    all_product = Product.all_products(cursor)
    if not all_product:
        return jsonify({
            'error':'No Products Found...'
        }),404
    return jsonify(all_product),200