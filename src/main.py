from fastapi import FastAPI

from src.applications.router import main_router


def web_app_factory() -> FastAPI:
    app = FastAPI(docs_url="/api/docs")
    app.include_router(main_router)
    return app
