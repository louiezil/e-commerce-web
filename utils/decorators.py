from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from connection import get_conn
from models.user_model import User
from flask import jsonify


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())

        conn = get_conn()
        cursor = conn.cursor()

        user = User.find_user_by_id(
            cursor,
            user_id,
        )
        if user and user.is_admin:
            return fn(*args, **kwargs)
        return jsonify({ "error": "Admin Only"}),403
    return wrapper