from fastapi import FastAPI
from mirel.infrastructure.store.sqlalchemy.connect import (
    create_session_factory,
)
from mirel.infrastructure.store.cloud.service import YandexDiskService
from mirel.infrastructure.images import ImageEditorImpl
from mirel.config.settings import Settings
from mirel.presentation.api.di.stubs import (
    provide_sqlalchemy_session_stub,
    provide_cloud_service_stub,
    provide_settings_stub,
    provide_product_create_handler_stub,
    provide_product_get_all_handler_stub,
    provide_product_get_handler_stub,
    provide_product_get_by_filters_handler_stub,
    provide_article_create_handler_stub,
    provide_article_get_all_handler_stub,
    provide_article_get_handler_stub,
    provide_image_editor_stub,
    provide_image_get_handler_stub,
)
from mirel.presentation.api.di.provides import (
    provide_product_create_handler,
    provide_product_get_all_handler,
    provide_product_get_handler,
    provide_product_get_by_filters_handler,
    provide_article_create_handler,
    provide_article_get_all_handler,
    provide_article_get_handler,
    provide_image_get_handler,
)


def setup_di(app: FastAPI, settings: Settings):
    session_factory = create_session_factory(settings.postgres.url)
    cloud = YandexDiskService(settings)
    image_editor = ImageEditorImpl(settings.path_to_folder_for_save_image)

    app.dependency_overrides.update(
        {
            provide_sqlalchemy_session_stub: session_factory,
            provide_cloud_service_stub: lambda: cloud,
            provide_settings_stub: lambda: settings,
            provide_image_editor_stub: lambda: image_editor,
        }
    )
    handlers = {
        provide_product_create_handler_stub: provide_product_create_handler,
        provide_product_get_all_handler_stub: provide_product_get_all_handler,
        provide_product_get_handler_stub: provide_product_get_handler,
        provide_product_get_by_filters_handler_stub: provide_product_get_by_filters_handler,
        provide_article_create_handler_stub: provide_article_create_handler,
        provide_article_get_all_handler_stub: provide_article_get_all_handler,
        provide_article_get_handler_stub: provide_article_get_handler,
        provide_image_get_handler_stub: provide_image_get_handler,
    }
    app.dependency_overrides.update(handlers)
