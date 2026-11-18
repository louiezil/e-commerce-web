from datetime import datetime


class Product:
    def __init__(
        self,
        product_name,
        price,
        in_stock=None,
        date_created=None,
        date_updated=None,
        product_id=None,
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.in_stock = in_stock
        self.date_created = date_created
        self.date_updated = date_updated

    def save_update(self, conn, cursor):
        if not self.product_id:
            try:
                cursor.execute(
                    "INSERT INTO products (product_name,price,in_stock,date_updated)VALUES(?,?,?,?)",
                    (
                        self.product_name,
                        self.price,
                        self.in_stock,
                        datetime.now().isoformat(),
                    ),
                )
                conn.commit()
                self.product_id = cursor.lastrowid
                return True
            except Exception as e:
                print(f"error saving product:{e}")
                return False
        try:
            cursor.execute(
                "UPDATE products SET product_name=?,price=?,in_stock=?,date_updated=? WHERE id =?",
                (
                    self.product_name,
                    self.price,
                    self.in_stock,
                    datetime.now().isoformat(),
                    self.product_id,
                ),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"error updating product:{e}")
            return False

    @classmethod
    def find_product(cls, cursor, product_id):
        try:
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()
            if not product:
                return None
            (
                product_id,
                product_name,
                price,
                in_stock,
                date_created,
                date_updated,
            ) = product
            return cls(
                product_id=product_id,
                product_name=product_name,
                price=price,
                in_stock=in_stock,
                date_created=date_created,
                date_updated=date_updated,
            )

        except Exception as e:
            print(f"error finding product:{e}")
            return None

   
    def convert(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "in_stock": self.in_stock,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }

    @classmethod
    def all_products(cls, cursor):
        try:
            cursor.execute(
                """
        SELECT products.*
        FROM products
        WHERE products.in_stock >= ?
        ORDER BY products.date_created DESC
        """,
                (1,),
            )
            products = cursor.fetchall()
            if not products:
                return []
            return [
                cls(
                    product_id=product_id,
                    product_name=product_name,
                    price=price,
                    in_stock=in_stock,
                    date_created=date_created,
                    date_updated=date_updated,
                ).convert()
                for (
                    product_id,
                    product_name,
                    price,
                    in_stock,
                    date_created,
                    date_updated,
                ) in products
            ]
        except Exception as e:
            print(f"error fetching all posts:{e}")
            return []
