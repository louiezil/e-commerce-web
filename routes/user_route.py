from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from connection import get_conn
from models.user_model import User
from werkzeug.security import generate_password_hash

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/api/user",
)


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def user():
    user_id = int(get_jwt_identity())
    conn = get_conn()
    cursor = conn.cursor()

    user = User.find_user_by_id(
        cursor,
        user_id,
    )
    if not user:
        return jsonify({"error": "profile Not Found..."}), 404
    return jsonify(user.convert()), 200


@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update():
    conn = get_conn()
    cursor = conn.cursor()

    user_id = int(get_jwt_identity())

    user = User.find_user_by_id(
        cursor,
        user_id,
    )
    if not user:
        return jsonify({"error": "User Not Found..."}), 404

    data = request.get_json()
    user.username = data["username"] if data.get("username") else user.username
    user.email = data["email"] if data.get("email") else user.email
    user.password = (
        generate_password_hash(data["password"])
        if data.get("password")
        else user.password
    )

    user.save_update(conn, cursor)
    return (
        jsonify(
            user.find_user_by_id(
                cursor,
                user_id,
            ).convert()
        ),
        200,
    )
