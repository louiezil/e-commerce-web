from datetime import datetime
from models.cart_item_model import Cart_item


class Cart:
    def __init__(
        self,
        user_id,
        cart_id=None,
        is_active=None,
        date_created=None,
        date_updated=None,
        username=None,
        cart_items=[],
        total_price=None,
    ):
        self.user_id = user_id
        self.cart_id = cart_id
        self.is_active = is_active
        self.date_created = date_created
        self.date_updated = date_updated
        self.username = username
        self.cart_items = cart_items
        self.total_price = total_price

    # this has an error to be fixed
    @classmethod
    def find_cart(cls, cursor, user_id, is_active=1):
        try:
            cursor.execute(
                """
        SELECT carts.*,
                        users.username AS username
                    
        FROM carts
        JOIN users ON users.id = carts.user_id
        WHERE carts.user_id =? AND carts.is_active =?
        """,
                (
                    user_id,
                    is_active,
                ),
            )
            active_cart = cursor.fetchone()
            if not active_cart:
                return None
            (
                cart_id,
                user_id,
                is_active,
                date_created,
                date_updated,
                username,
            ) = active_cart

            cart_items = Cart_item.find_cart_items(cursor, cart_id)
            total_price = []
            if cart_items:
                for each_item in cart_items:
                    each_price = each_item.get("price")
                    quantity = each_item.get("quantity")
                    total = each_price * quantity
                    total_price.append(total)

            return cls(
                cart_id=cart_id,
                user_id=user_id,
                is_active=is_active,
                date_created=date_created,
                date_updated=date_updated,
                cart_items=cart_items,
                username=username,
                total_price=sum(total_price) if total_price else 0,
            )
        except Exception as e:
            return None

    @classmethod
    def find_cart_by_id(cls, cursor, cart_id):
        try:
            cursor.execute(
                """
        SELECT carts.*,
                        users.username AS username
                    
        FROM carts
        JOIN users ON users.id = carts.user_id
        WHERE carts.user_id =?
        """,
                (cart_id,),
            )
            active_cart = cursor.fetchone()
            if not active_cart:
                return None
            (
                cart_id,
                user_id,
                is_active,
                date_created,
                date_updated,
                username,
            ) = active_cart

            cart_items = Cart_item.find_cart_items(cursor, cart_id)
            total_price = []
            if cart_items:
                for each_item in cart_items:
                    each_price = each_item.get("price")
                    quantity = each_item.get("quantity")
                    total = each_price * quantity
                    total_price.append(total)
            return cls(
                cart_id=cart_id,
                user_id=user_id,
                is_active=is_active,
                date_created=date_created,
                date_updated=date_updated,
                cart_items=cart_items,
                username=username,
                total_price=sum(total_price) if total_price else 0,
            )
        except Exception as e:
            return None

    def convert(self):
        return {
            "cart_id": self.cart_id,
            "user_id": self.user_id,
            "is_active": self.is_active,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "cart_items": self.cart_items,
            "user_name": self.username,
            "total_price": self.total_price,
        }

    def active_in_active(self, cursor, conn):
        if not self.cart_id:
            try:
                cursor.execute(
                    "INSERT INTO carts (user_id,date_updated)VALUES(?,?)",
                    (
                        self.user_id,
                        datetime.now().isoformat(),
                    ),
                )
                conn.commit()
                self.cart_id = cursor.lastrowid
                return True
            except Exception as e:
                print(f"error saving cart...")
                return False

        try:
            self.is_active = 0 if self.is_active is None else self.is_active
            cursor.execute(
                "UPDATE carts SET is_active = ?, date_updated = ? WHERE id =?",
                (
                    self.is_active,
                    datetime.now().isoformat(),
                    self.cart_id,
                ),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"error de-activating cart...")
            return False
