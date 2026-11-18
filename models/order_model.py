from datetime import datetime
from models.order_item_model import Order_item


class Order:
    def __init__(
        self,
        user_id,
        total_amount,
        ordered_items=[],
        status_id=1,
        status_name=None,
        order_id=None,
        date_created=None,
        date_updated=None,
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.ordered_items = ordered_items
        self.total_amount = total_amount
        self.date_created = date_created
        self.date_updated = date_updated
        self.status_id = status_id
        self.status_name = status_name

    def save_update(self, conn, cursor):
        if not self.order_id:
            try:
                cursor.execute(
                    "INSERT INTO orders(user_id,status_id,total_amount,date_updated)VALUES(?,?,?,?)",
                    (
                        self.user_id,
                        self.status_id,
                        self.total_amount,
                        datetime.now().isoformat(),
                    ),
                )

                self.order_id = cursor.lastrowid
                conn.commit()

                for each in self.ordered_items:
                    product_id = each.get("product_id")
                    product_name = each.get("product_name")
                    price_at_purchase = each.get("price")
                    quantity = each.get("quantity")

                    save = Order_item(
                        product_id,
                        product_name,
                        self.order_id,
                        quantity,
                        price_at_purchase,
                    ).save(conn, cursor)
                    if not save:
                        return False
                return True

            except Exception as e:
                print(f"error saving order:{e}")
                return False
        try:
            cursor.execute(
                "UPDATE orders SET status_id =? ,date_updated =? WHERE id =?",
                (
                    self.status_id,
                    datetime.now().isoformat(),
                    self.order_id,
                ),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"error updating Order:{e}")
            return False

    @classmethod
    def find_order(cls, cursor, order_id):
        try:
            cursor.execute(
                """
        SELECT orders.*,
                            status.name AS status_name
        
        FROM orders
        LEFT JOIN status ON status.id = orders.status_id
        WHERE orders.id = ?
        """,
                (order_id,),
            )
            order = cursor.fetchone()
            if not order:
                return None
            (
                order_id,
                user_id,
                status_id,
                total_amount,
                date_created,
                date_updated,
                status_name,
            ) = order
            order_items = Order_item.find_ordered_items(cursor, order_id)

            return cls(
                user_id=user_id,
                total_amount=total_amount,
                status_id=status_id,
                status_name=status_name,
                order_id=order_id,
                date_created=date_created,
                date_updated=date_updated,
                ordered_items=order_items,
            )

        except Exception as e:
            print(f"error finding order:{e}")
            return None

    @classmethod
    def find_orders(cls, cursor, user_id):
        try:
            # was trying to join the order items but lol
            cursor.execute(
                """
        SELECT orders.*,
                            status.name AS status_name
        
        FROM orders
        LEFT JOIN status ON status.id = orders.status_id
        WHERE orders.user_id = ?
        """,
                (user_id,),
            )
            orders = cursor.fetchall()
            if not orders:
                return []
            return [
                cls(
                    user_id=user_id,
                    total_amount=total_amount,
                    status_id=status_id,
                    status_name=status_name,
                    order_id=order_id,
                    date_created=date_created,
                    date_updated=date_updated,
                    ordered_items=Order_item.find_ordered_items(cursor,ordered_items_order_id=order_id),
                )
                for (
                    order_id,
                    user_id,
                    status_id,
                    total_amount,
                    date_created,
                    date_updated,
                    status_name,
                ) in orders
            ]


        except Exception as e:
            print(f"error finding orders:{e}")
            return []

    def convert(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "status_id": self.status_id,
            "status_name": self.status_name,
            "ordered_items": self.ordered_items,
            "total_amount": self.total_amount,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }
