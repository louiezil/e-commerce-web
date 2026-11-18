class status:
    def __init__(
        self,
        name,
        status_id=None,
    ):
        self.name = name
        self.status_id = status_id

    def save_update(self, cursor, conn):
        if not self.status_id:
            try:
                cursor.execute("INSERT INTO status (name)VALUES(?)", (self.name,))
                conn.commit()
                self.status_id = cursor.lastrowid

            except Exception as e:
                print(f"error saving status:{e}")
                return False
        try:
            cursor.execute(
                "UPDATE status SET name =? WHERE id =?",
                (
                    self.name,
                    self.status_id,
                ),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"error updating status: {e}")
            return False

        
