from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from .db import db_conn
from .utils import generate_captcha_text, now_str

router = APIRouter(prefix="/api")


@router.get("/products")
async def get_products():
    with db_conn() as conn:
        rows = conn.execute(
            """
            SELECT title, price, image, category, rating, rating_count, delivery, link
            FROM products
            ORDER BY id ASC
            """
        ).fetchall()
        return [dict(r) for r in rows]


@router.get("/captcha")
async def get_captcha(response: Response):
    code = generate_captcha_text()
    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='140' height='50'>
      <rect width='100%' height='100%' fill='#f8f9fa'/>
      <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle'
            font-family='Arial, sans-serif' font-size='22' fill='#333' letter-spacing='3'>
        {code}
      </text>
    </svg>
    """
    response = Response(content=svg, media_type="image/svg+xml")
    response.set_cookie("captcha_code", code, httponly=False, max_age=300)
    return response


@router.post("/login")
async def login(request: Request):
    data = await request.json()
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    captcha = (data.get("captcha") or "").strip()

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required.")

    cookie_code = request.cookies.get("captcha_code", "")
    if not captcha or captcha.upper() != cookie_code.upper():
        raise HTTPException(status_code=400, detail="Invalid CAPTCHA.")

    with db_conn() as conn:
        row = conn.execute(
            "SELECT id, username FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="Invalid username or password.")

        return {"username": row["username"], "id": row["id"]}


@router.post("/signup")
async def signup(request: Request):
    data = await request.json()
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="All fields are required.")

    with db_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            (email,),
        ).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered.")

        conn.execute(
            "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
            (name, email, password),
        )
        conn.commit()

        row = conn.execute(
            "SELECT id, username FROM users WHERE username = ?",
            (email,),
        ).fetchone()

        return {"username": row["username"], "id": row["id"]}


@router.get("/account")
async def account_details(user_id: int | None = None):
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id.")
    with db_conn() as conn:
        row = conn.execute(
            "SELECT id, name, username FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"id": row["id"], "name": row["name"], "username": row["username"]}


@router.get("/orders")
async def orders(user_id: int | None = None):
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id.")
    with db_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, item, amount, status, created_at
            FROM orders
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


@router.get("/payments")
async def payments(user_id: int | None = None):
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id.")
    with db_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, order_id, amount, method, status, created_at
            FROM payments
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


@router.post("/checkout")
async def checkout(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    items = data.get("items") or []
    total = (data.get("total") or "").strip()
    method = (data.get("method") or "").strip()
    upi_id = (data.get("upi_id") or "").strip()
    address = (data.get("address") or "").strip()

    if not user_id or not items or not total or not method:
        raise HTTPException(status_code=400, detail="Missing checkout data.")

    if method.upper() == "UPI" and not upi_id:
        raise HTTPException(status_code=400, detail="UPI ID is required.")
    if not address:
        raise HTTPException(status_code=400, detail="Delivery address is required.")

    item_label = f"{len(items)} items"
    created_at = now_str()

    with db_conn() as conn:
        conn.execute(
            """
            INSERT INTO orders (user_id, item, amount, status, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, item_label, total, "PAID", created_at),
        )
        order_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        conn.execute(
            """
            INSERT INTO payments (user_id, order_id, amount, method, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, order_id, total, method.upper(), "SUCCESS", created_at),
        )
        conn.commit()

    return {"order_id": order_id, "status": "PAID"}
