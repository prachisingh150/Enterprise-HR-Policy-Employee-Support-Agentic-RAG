from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.config import get_settings, BASE_DIR


def create_app() -> FastAPI:
    settings = get_settings()

    from app.api.routes import router
    from app.core.logging import configure_logging
    from app.services.audit import init_db

    configure_logging()
    init_db()

    application = FastAPI(title=settings.app_name, version="1.0.0")
    application.include_router(router)
    application.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

    @application.get("/", response_class=HTMLResponse)
    def home(request: Request):
        return templates.TemplateResponse(
            "index.html", {"request": request, "app_name": settings.app_name}
        )

    return application


app = create_app()
