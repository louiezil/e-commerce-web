from datetime import datetime


class User:
    def __init__(
        self,
        username,
        email,
        password,
        is_admin=None,
        is_active=None,
        date_created=None,
        date_updated=None,
        user_id=None,
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.date_created = date_created
        self.date_updated = date_updated
        self.is_admin = 0 if not is_admin else is_admin
        self.is_active = 1 if not is_active else is_active

    def save_update(self, conn, cursor):
        if not self.user_id:
            try:
                cursor.execute(
                    "INSERT INTO users (username,email,password,is_active,is_admin,date_updated)VALUES(?,?,?,?,?,?)",
                    (
                        self.username,
                        self.email,
                        self.password,
                        self.is_active,
                        self.is_admin,
                        datetime.now().isoformat(),
                    ),
                )
                conn.commit()
                self.user_id = cursor.lastrowid
                return True
            except Exception as e:
                print(f"error saving User : {e}")
                return False

        try:
            cursor.execute(
                "UPDATE users SET username =?,email=?,password=?,is_active=?,is_admin =?,date_updated=? WHERE id =?",
                (
                    self.username,
                    self.email,
                    self.password,
                    self.is_active,
                    self.is_admin,
                    datetime.now().isoformat(),
                    self.user_id,
                ),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"error saving User : {e}")
            return False

    @classmethod
    def find_user(cls, cursor, email):
        try:
            cursor.execute(
                "SELECT * FROM users WHERE email = ?",
                (
                    email,
                ),
            )
            user = cursor.fetchone()
            if not user:
                return None
            (
                user_id,
                username,
                email,
                password,
                is_admin,
                is_active,
                date_created,
                date_updated,
            ) = user
            return cls(
                user_id=user_id,
                username=username,
                email=email,
                password=password,
                is_admin=is_admin,
                is_active=is_active,
                date_created=date_created,
                date_updated=date_updated,
            )
        except Exception as e:
            print(f"error finding_User : {e}")
            return None

    @classmethod
    def find_user_by_id(cls, cursor, user_id):
        try:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            if not user:
                return None
            (
                user_id,
                username,
                email,
                password,
                is_admin,
                is_active,
                date_created,
                date_updated,
            ) = user
            return cls(
                user_id=user_id,
                username=username,
                email=email,
                password=password,
                is_admin=is_admin,
                is_active=is_active,
                date_created=date_created,
                date_updated=date_updated,
            )
        except Exception as e:
            print(f"error finding_User byId : {e}")
            return None

    def convert(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": "******",
            "is_admin": self.is_admin,
            "is_active": self.is_active,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }
