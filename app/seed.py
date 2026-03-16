from .db import db_conn


def ensure_products(conn) -> None:
    products = [
        (
            "Shimla Apples",
            "Rs 250/kg",
            "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
            "fruits",
            4.8,
            120,
            "Next day",
            "/cart.html",
        ),
        (
            "Nagpur Oranges",
            "Rs 120/kg",
            "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
            "fruits",
            4.7,
            95,
            "Next day",
            "/cart.html",
        ),
        (
            "Maharashtra Strawberries",
            "Rs 400/kg",
            "https://images.unsplash.com/photo-1559181567-c3190ca9959b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
            "fruits",
            4.9,
            210,
            "Same day",
            "/cart.html",
        ),
        (
            "Robusta Bananas",
            "Rs 60/dozen",
            "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
            "fruits",
            4.5,
            180,
            "Next day",
            "/cart.html",
        ),
        (
            "Fresh Carrots",
            "Rs 40/kg",
            "https://images.unsplash.com/photo-1518977676601-b53f82aba655?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
            "vegetables",
            4.6,
            85,
            "Next day",
            "/cart.html",
        ),
        (
            "Fresh Broccoli",
            "Rs 80/piece",
            "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
            "vegetables",
            4.7,
            110,
            "Next day",
            "/cart.html",
        ),
        (
            "Palak (Spinach)",
            "Rs 20/bunch",
            "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
            "vegetables",
            4.8,
            75,
            "Same day",
            "/cart.html",
        ),
        (
            "Nasik Onions",
            "Rs 30/kg",
            "https://t3.ftcdn.net/jpg/10/70/98/44/360_F_1070984497_Q98FNQiXfDSK0IG5jz6moyAUj6nYrop4.jpg",
            "vegetables",
            4.6,
            92,
            "Next day",
            "/cart.html",
        ),
        (
            "Hybrid Chilli Seeds",
            "Rs 350/pack",
            "https://agriplexindia.com/cdn/shop/files/Armour-F1-Hybrid-Chilli-Seeds.png?v=1743241709",
            "seeds",
            4.9,
            210,
            "Next day",
            "/cart.html",
        ),
        (
            "Balaji Seeds",
            "Rs 120/pack",
            "https://tiimg.tistatic.com/fp/1/007/589/high-effective-natural-pure-agriculture-balaji-seeds-color-black-in-pack-062.jpg",
            "seeds",
            4.8,
            156,
            "Same day",
            "/cart.html",
        ),
        (
            "Hybrid Bajra Seeds",
            "Rs 150/pack",
            "https://tiimg.tistatic.com/fp/1/007/732/agro-9460-hybrid-bajra-seed-for-cultivation-purposes-packaging-type-packet-25-moisture-856.jpg",
            "seeds",
            4.9,
            88,
            "Next day",
            "/cart.html",
        ),
        (
            "Cotton Seeds",
            "Rs 250/pack",
            "https://5.imimg.com/data5/SELLER/Default/2022/4/ZP/KX/RI/101068562/dried-cotton-seeds-500x500.jpeg",
            "seeds",
            4.7,
            134,
            "Same day",
            "/cart.html",
        ),
        (
            "hybrid bajra seeds",
            "$1.99/pack",
            "https://tiimg.tistatic.com/fp/1/007/732/agro-9460-hybrid-bajra-seed-for-cultivation-purposes-packaging-type-packet-25-moisture-856.jpg",
            "dairy",
            4.9,
            88,
            "Next day",
            "/cart.html",
        ),
        (
            "cotton seeds",
            "$2.99/pack",
            "https://5.imimg.com/data5/SELLER/Default/2022/4/ZP/KX/RI/101068562/dried-cotton-seeds-500x500.jpeg",
            "dairy",
            4.7,
            134,
            "Same day",
            "/cart.html",
        ),
        (
            "Filia oil",
            "$2.49/bunch",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKVWWmaJ7LoGrvc_KKXK6cZaDkPTGRByWsag&s",
            "herbs",
            4.7,
            65,
            "Next day",
            "/cart.html",
        ),
        (
            "All in one",
            "$10.99/bunch",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDOpYdR-h1b3aWgnekom8Co9exRMDoFN81HQ&s",
            "herbs",
            4.5,
            72,
            "Same day",
            "/cart.html",
        ),
        (
            "super 80",
            "$1.79/1L",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsxzy2-p0dhJTPbJoyUABTO792cYwn-CaW3nQ-cAkI3QKeLkWk1G8sS8p_R5Dej8WOKSE&usqp=CAU",
            "herbs",
            4.6,
            58,
            "Next day",
            "/cart.html",
        ),
        (
            "Herbicide Bactericide Foliar",
            "$2.29/bunch",
            "https://image.made-in-china.com/2f0j00OVGkcAClwLod/Agriculture-Chemical-Spray-Herbicide-Bactericide-Foliar-Fertilizer-Plant-Growth-Regulator-Adjuvant-3240.webp",
            "herbs",
            4.8,
            49,
            "Same day",
            "/cart.html",
        ),
    ]

    existing = {
        row["title"] for row in conn.execute("SELECT title FROM products").fetchall()
    }
    to_insert = [p for p in products if p[0] not in existing]
    if not to_insert:
        return

    conn.executemany(
        """
        INSERT INTO products
        (title, price, image, category, rating, rating_count, delivery, link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        to_insert,
    )
    conn.commit()


def seed_users(conn) -> None:
    conn.execute(
        "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
        ("Demo User", "user@example.com", "password"),
    )
    conn.commit()


def init_db() -> None:
    with db_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price TEXT NOT NULL,
                image TEXT NOT NULL,
                category TEXT NOT NULL,
                rating REAL NOT NULL,
                rating_count INTEGER NOT NULL,
                delivery TEXT NOT NULL,
                link TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item TEXT NOT NULL,
                amount TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                order_id INTEGER,
                amount TEXT NOT NULL,
                method TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
            """
        )
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(users)")}
        if "name" not in cols:
            conn.execute("ALTER TABLE users ADD COLUMN name TEXT")
            conn.commit()

        ensure_products(conn)

        cur = conn.execute("SELECT COUNT(*) AS c FROM users")
        if cur.fetchone()["c"] == 0:
            seed_users(conn)
