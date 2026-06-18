from __future__ import annotations

import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.routes import router
from light_text_process.capabilities import build_capabilities
from product_paths import STATIC_DIR, TEMPLATES_DIR


templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def create_app() -> FastAPI:
    app = FastAPI(title="Light Text Process Web")
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    app.include_router(router)

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "product_name": "Light Text Process",
                "capabilities": build_capabilities(),
                "asset_version": _asset_version(),
            },
        )

    return app


def _asset_version() -> int:
    asset_paths = [
        STATIC_DIR / "css" / "app.css",
        STATIC_DIR / "data" / "examples.json",
        STATIC_DIR / "js" / "app.js",
    ]
    existing = [path.stat().st_mtime for path in asset_paths if path.exists()]
    if not existing:
        return 0
    return int(max(existing))


app = create_app()


def main() -> None:
    host = os.getenv("LIGHT_TEXT_PROCESS_WEB_HOST", "127.0.0.1").strip() or "127.0.0.1"
    try:
        port = int(os.getenv("LIGHT_TEXT_PROCESS_WEB_PORT", "8011"))
    except ValueError:
        port = 8011
    uvicorn.run(app, host=host, port=max(1, min(65535, port)))


if __name__ == "__main__":
    main()
