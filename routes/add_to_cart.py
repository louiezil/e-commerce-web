from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from connection import get_conn

add_to_cart_bp = Blueprint(
    "add_to_cart",
    __name__,
    url_prefix="/api/product",
)


