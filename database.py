def create_tables(conn, cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0 NOT NULL CHECK( is_admin IN (0,1)),
        is_active INTEGER DEFAULT 1 CHECK (is_active IN ( 0,1)) NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP
        
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS status(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price INTEGER NOT NULL,
        in_stock INTEGER NOT NULL DEFAULT 0,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP 
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        is_active INTEGER DEFAULT 1 CHECK(is_active IN (0,1)) NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL   
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        status_id INTEGER,
        total_amount INTEGER,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
        FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE RESTRICT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        product_name TEXT,
        order_id INTEGER, 
        quantity INTEGER,
        price_at_purchase INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE, 
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
    )
    """)

    conn.commit()


# products      id, name, price, stock, date_created, date_updated
# carts         id, user_id FK, is_active, date_created, date_updated
# cart_items    id, cart_id FK, product_id FK, quantity
# orders        id, user_id FK, total, status, date_created, date_updated
# order_items   id, order_id FK, product_id FK, quantity, price_at_purchase
