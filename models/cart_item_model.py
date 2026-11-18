class Cart_item:
    def __init__(
        self,
        product_id,
        cart_id,
        quantity=None,
        cart_item_id=None,
        product_name=None,
        price=None,
        in_stock=None,
    ):
        self.product_id = product_id
        self.cart_id = cart_id
        self.quantity = 1 if not quantity else quantity
        self.cart_item_id = cart_item_id
        self.product_name = product_name
        self.price = price
        self.in_stock = in_stock

    def save_update(self, cursor, conn):

        if not self.cart_item_id:
            try:
                cursor.execute(
                    " INSERT INTO cart_items(cart_id,quantity,product_id)VALUES(?,?,?)",
                    (
                        self.cart_id,
                        self.quantity,
                        self.product_id,
                    ),
                )
                conn.commit()
                self.cart_item_id = cursor.lastrowid
                return True
            except Exception as e:
                print(f"error adding cart item:{e}")
                return False
        try:
            cursor.execute(
                "UPDATE cart_items SET quantity = ? WHERE id = ?",
                (
                    self.quantity,
                    self.cart_item_id,
                ),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"error updating cart item:{e}")
            return False

        # else increase the quantity

    @classmethod
    def find_cart_item(cls, cursor, cart_item_id):
        try:
            cursor.execute(
                # "SELECT * FROM cart_items WHERE cart_id =? AND product_id ?",
                """
        SELECT cart_items.*,
                            products.product_name AS product_name,
                            products.price AS  price,
                            products.in_stock AS  in_stock
        FROM cart_items
        JOIN products ON products.id = cart_items.product_id
        WHERE cart_items.id =?
        """,
                (cart_item_id,),
            )

            cart_item = cursor.fetchone()
            if not cart_item:
                return None
            (
                cart_item_id,
                cart_id,
                product_id,
                quantity,
                product_name,
                price,
                in_stock,
            ) = cart_item

            return cls(
                product_id=product_id,
                cart_id=cart_id,
                quantity=quantity,
                cart_item_id=cart_item_id,
                product_name=product_name,
                price=price,
                in_stock=in_stock,
            )
        except Exception as e:
            print(f"error finding cart_item:{e}")
            return None

    @classmethod
    def find_cart_item_cartId_and_product_id(cls, cursor, cart_id, product_id):
        try:
            cursor.execute(
                # "SELECT * FROM cart_items WHERE cart_id =? AND product_id ?",
                """
        SELECT cart_items.*,
                            products.product_name AS product_name,
                            products.price AS  price,
                            products.in_stock AS  in_stock
        FROM cart_items
        JOIN products ON products.id = cart_items.product_id
        WHERE cart_items.cart_id =? AND cart_items.product_id = ?
        """,
                (
                    cart_id,
                    product_id,
                ),
            )

            cart_item = cursor.fetchone()
            if not cart_item:
                return None
            (
                cart_item_id,
                cart_id,
                product_id,
                quantity,
                product_name,
                price,
                in_stock,
            ) = cart_item

            return cls(
                product_id=product_id,
                cart_id=cart_id,
                quantity=quantity,
                cart_item_id=cart_item_id,
                product_name=product_name,
                price=price,
                in_stock=in_stock,
            )
        except Exception as e:
            print(f"error finding cart_item:{e}")
            return None

    @classmethod
    def find_cart_items(cls, cursor, cart_id):
        try:
            cursor.execute(
                # "SELECT * FROM cart_items WHERE cart_id =? AND product_id ?",
                """
        SELECT cart_items.*,
                            products.product_name AS product_name,
                            products.price AS  price,
                            products.in_stock AS  in_stock
        FROM cart_items
        JOIN products ON products.id = cart_items.product_id
        WHERE cart_items.cart_id =?
        """,
                (cart_id,),
            )

            cart_items = cursor.fetchall()
            if not cart_items:
                return []
            return [
                cls(
                    product_id=product_id,
                    cart_id=cart_id,
                    quantity=quantity,
                    cart_item_id=cart_item_id,
                    product_name=product_name,
                    price=price,
                    in_stock=in_stock,
                ).convert()
                for (
                    cart_item_id,
                    cart_id,
                    product_id,
                    quantity,
                    product_name,
                    price,
                    in_stock,
                ) in cart_items
            ]
        except Exception as e:
            print(f"error finding cart_item:{e}")
            return []

    def convert(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "quantity": self.quantity,
            "in_stock": self.in_stock,
            "cart_item_id": self.cart_item_id,
            "cart_id": self.cart_id,
        }
