class Order_item:
    def __init__(
        self,
        product_id,
        product_name,
        order_id,
        quantity,
        price_at_purchase,
        ordered_item_id=None,
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.order_id = order_id
        self.quantity = quantity
        self.price_at_purchase = price_at_purchase
        self.ordered_item_id = ordered_item_id

    def save(self, conn, cursor):
            try:
                cursor.execute(
                    "INSERT INTO order_items (product_id,product_name,order_id,quantity,price_at_purchase)VALUES(?,?,?,?,?)",
                    (
                        self.product_id,
                        self.product_name,
                        self.order_id,
                        self.quantity,
                        self.price_at_purchase,
                    ),
                )
                self.ordered_item_id = cursor.lastrowid
                conn.commit()
                return True

            except Exception as e:
                print(f'error saving Order_item:{e}')
                return False

    @classmethod
    def find_ordered_item(cls, cursor, ordered_item_id):
        try:
            cursor.execute("SELECT * FROM order_items WHERE id =?", (ordered_item_id,))
            ordered_item = cursor.fetchone()
            if not ordered_item:
                return None
            (
                ordered_item_id,
                product_id,
                product_name,
                order_id,
                quantity,
                price_at_purchase,
            ) = ordered_item
            return cls(
                ordered_item_id=ordered_item_id,
                product_id=product_id,
                product_name=product_name,
                order_id=order_id,
                quantity=quantity,
                price_at_purchase=price_at_purchase,
            )
        except Exception as e:
            print(f"error finding ordered_item")
            return None

    @classmethod
    def find_ordered_items(cls, cursor, ordered_items_order_id):
        try:
            cursor.execute(
                "SELECT * FROM order_items WHERE order_id =?", (ordered_items_order_id,)
            )
            ordered_items = cursor.fetchall()
            if not ordered_items:
                return []
            return [
                cls(
                    ordered_item_id=ordered_item_id,
                    product_id=product_id,
                    product_name=product_name,
                    order_id=order_id,
                    quantity=quantity,
                    price_at_purchase=price_at_purchase,
                ).convert()
                for (
                    ordered_item_id,
                    product_id,
                    product_name,
                    order_id,
                    quantity,
                    price_at_purchase,
                ) in ordered_items
            ]

        except Exception as e:
            print(f"error finding ordered_item")
            return None

    def convert(self):
        return {
            "ordered_item_id": self.ordered_item_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "order_id": self.order_id,
            "quantity": self.quantity,
            "price_at_purchase": self.price_at_purchase,
        }
