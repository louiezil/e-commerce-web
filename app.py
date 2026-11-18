from flask import Flask
from flask_jwt_extended import JWTManager
from connection import close_conn
from config import Config
from database import create_tables
import sqlite3
from routes.auth_route import auth_bp
from routes.user_route import user_bp
from routes.product_route import product_bp
from routes.add_to_cart import add_to_cart_bp
from routes.cart_route import cart_bp
from routes.order_route import order_bp
from models.status_model import status

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

with app.app_context():
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    conn.execute("PRAGMA foreign_keys=ON")
    create_tables(conn, cursor)

    names = ["pending", "paid", "Shipped", "Delivered"]

    # for each in names:
    #     status(name=each).save_update(cursor, conn)
    #     print(f"{each} registered")
    conn.close()


app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(add_to_cart_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)


app.teardown_appcontext(close_conn)

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
