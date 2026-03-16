from fastapi import APIRouter, HTTPException, Request

from .config import ADMIN_PASSWORD, ADMIN_TOKEN, ADMIN_USERNAME
from .db import db_conn

router = APIRouter(prefix="/api/admin")


def require_admin(request: Request) -> None:
    token = request.headers.get("X-Admin-Token") or ""
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/login")
async def admin_login(request: Request):
    data = await request.json()
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin credentials.")
    return {"username": username, "token": ADMIN_TOKEN}


@router.get("/products")
async def admin_products(request: Request):
    require_admin(request)
    with db_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, title, price, image, category, rating, rating_count, delivery, link
            FROM products
            ORDER BY id ASC
            """
        ).fetchall()
        return [dict(r) for r in rows]


@router.post("/products")
async def admin_create_product(request: Request):
    require_admin(request)
    data = await request.json()
    title = (data.get("title") or "").strip()
    price = (data.get("price") or "").strip()
    image = (data.get("image") or "").strip()
    category = (data.get("category") or "").strip()
    rating = float(data.get("rating") or 0)
    rating_count = int(data.get("rating_count") or 0)
    delivery = (data.get("delivery") or "Next day").strip()
    link = (data.get("link") or "/cart.html").strip()
    if not title or not price or not image or not category:
        raise HTTPException(status_code=400, detail="Missing required fields.")
    with db_conn() as conn:
        conn.execute(
            """
            INSERT INTO products
            (title, price, image, category, rating, rating_count, delivery, link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, price, image, category, rating, rating_count, delivery, link),
        )
        conn.commit()
    return {"status": "created"}


@router.put("/products/{product_id}")
async def admin_update_product(product_id: int, request: Request):
    require_admin(request)
    data = await request.json()
    fields = []
    values = []
    for key in ["title", "price", "image", "category", "rating", "rating_count", "delivery", "link"]:
        if key in data:
            fields.append(f"{key} = ?")
            values.append(data[key])
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update.")
    values.append(product_id)
    with db_conn() as conn:
        conn.execute(f"UPDATE products SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
    return {"status": "updated"}


@router.delete("/products/{product_id}")
async def admin_delete_product(product_id: int, request: Request):
    require_admin(request)
    with db_conn() as conn:
        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
    return {"status": "deleted"}
