from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from .open_api import set_custom_openapi
from mirel.presentation.api.di.di import setup_di
from mirel.presentation.api.routes import router
from mirel.infrastructure.store.sqlalchemy.models import (
    mapping as sqlalchemy_mapping,
)
from mirel.config.settings import Settings
from mirel.config.initialization import initial_initialization


def create_app() -> FastAPI:
    settings = Settings()

    app = FastAPI(
        root_path=settings.root_path,
        root_path_in_servers=True,
        docs_url=settings.docs_url,
        port=settings.port,
    )
    setup_di(app, settings)
    sqlalchemy_mapping()

    app.include_router(router)
    set_custom_openapi(app, settings)

    return app


app = create_app()
