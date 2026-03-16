import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from .utils import html_path

router = APIRouter()


@router.get("/")
async def home():
    return FileResponse(html_path("formerproject.html"))


@router.get("/login")
async def login_page():
    return FileResponse(html_path("formerlogin.html"))


@router.get("/formerproject.html")
async def former_project():
    return FileResponse(html_path("formerproject.html"))


@router.get("/formerlogin.html")
async def former_login():
    return FileResponse(html_path("formerlogin.html"))


@router.get("/signup")
async def signup_page():
    return FileResponse(html_path("signup.html"))


@router.get("/signup.html")
async def signup_page_html():
    return FileResponse(html_path("signup.html"))


@router.get("/shopl.html")
async def shop_page():
    return FileResponse(html_path("shopl.html"))


@router.get("/cart.html")
async def cart_page():
    return FileResponse(html_path("cart.html"))


@router.get("/account.html")
async def account_page():
    return FileResponse(html_path("account.html"))


@router.get("/orders.html")
async def orders_page():
    return FileResponse(html_path("orders.html"))


@router.get("/payments.html")
async def payments_page():
    return FileResponse(html_path("payments.html"))


@router.get("/admin_login.html")
async def admin_login_page():
    return FileResponse(html_path("admin_login.html"))


@router.get("/admin_dashboard.html")
async def admin_dashboard_page():
    return FileResponse(html_path("admin_dashboard.html"))


@router.get("/{page}.html")
async def any_html_page(page: str):
    path = html_path(f"{page}.html")
    if os.path.isfile(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="Not Found")
