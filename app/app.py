from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes_api import router as api_router
from .routes_admin import router as admin_router
from .routes_pages import router as pages_router
from .seed import init_db


def create_app() -> FastAPI:
    app = FastAPI(title="FarmFresh Demo")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup():
        init_db()

    app.include_router(pages_router)
    app.include_router(api_router)
    app.include_router(admin_router)
    return app


app = create_app()
