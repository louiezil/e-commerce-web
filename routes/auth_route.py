from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, create_access_token
from models.user_model import User
from connection import get_conn
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth",
)


@auth_bp.route("/login", methods=["POST"])
def login():
    conn = get_conn()
    cursor = conn.cursor()
    data = request.get_json()

    email = data.get("email")
    password_str = data.get("password")

    if not email or not password_str:
        return jsonify({"error": "Invalid Input"}), 400
    elif "@" not in email:
        return jsonify({"error": "Invalid Email Address..."}), 400

    user = User.find_user(
        cursor,
        email,
    )

    if not user:
        return jsonify({"error": "user Not found..."}), 404
    pass_confirm = check_password_hash(
        user.password,
        password_str,
    )
    if pass_confirm:
        token = create_access_token(identity=str(user.user_id))
        return jsonify({"token": token}), 200
    return jsonify({"error": "password Incorrect..."}), 401


@auth_bp.route("/register", methods=["POST"])
def register():
    conn = get_conn()
    cursor = conn.cursor()

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password_str = data.get("password")
    password_str_Repeated = data.get("password_repeated")

    if not username or not email or not password_str:
        return jsonify({"error": "Invalid Input"}), 400
    elif len(username) < 4:
        return jsonify({"error": "Input Too Short..."}), 400
    elif len(password_str) < 6:
        return jsonify({"error": " Password Too Short..."}), 400
    elif len(email) < 6:
        return jsonify({"error": " Email Address Too Short..."}), 400
    elif "@" not in email:
        return jsonify({"error": "Invalid Email Address..."}), 400
    elif password_str != password_str_Repeated:
        return jsonify({"error": "password MisMatch..."}), 422
    check_user = User.find_user(
        cursor,
        email,
    )
    if check_user:
        return jsonify({"error": "User Already Exist..."}), 409
    hash_pass = generate_password_hash(password_str)
    if User(
        username,
        email,
        hash_pass,
    ).save_update(
        conn,
        cursor,
    ):
        return (
            jsonify(
                User.find_user(
                    cursor,
                    email,
                ).convert()
            ),
            201,
        )
    return jsonify({"error": "server related Error"}), 500
