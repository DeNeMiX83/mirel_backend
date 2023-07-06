from fastapi import FastAPI
from mirel.infrastructure.store.sqlalchemy.connect import (
    create_session_factory,
)
from mirel.infrastructure.store.cloud.service import YandexDiskService
from mirel.infrastructure.images import ImageEditorImpl
from mirel.infrastructure.email import EmailSenderImpl
from mirel.config.settings import Settings
from mirel.presentation.api.di.stubs import (
    provide_sqlalchemy_session_stub,
    provide_cloud_service_stub,
    provide_settings_stub,
    provide_product_create_handler_stub,
    provide_product_add_image_handler_stub,
    provide_product_get_all_handler_stub,
    provide_product_get_handler_stub,
    provide_product_get_by_filters_handler_stub,
    provide_type_solution_create_handler_stub,
    provide_type_solution_get_all_handler_stub,
    provide_type_object_create_handler_stub,
    provide_type_object_get_all_handler_stub,
    provide_article_create_handler_stub,
    provide_article_get_all_handler_stub,
    provide_article_get_handler_stub,
    provide_image_get_handler_stub,
    provide_forwarding_feedback_handler_stub,
    provide_image_editor_stub,
    provide_email_sender_stub,
)
from mirel.presentation.api.di.provides import (
    provide_product_create_handler,
    provide_product_add_image_handler,
    provide_product_get_all_handler,
    provide_product_get_handler,
    provide_product_get_by_filters_handler,
    provide_type_solution_create_handler,
    provide_type_solution_get_all_handler,
    provide_type_object_create_handler,
    provide_type_object_get_all_handler,
    provide_article_create_handler,
    provide_article_get_all_handler,
    provide_article_get_handler,
    provide_image_get_handler,
    provide_forwarding_feedback_handler,
)


def setup_di(app: FastAPI, settings: Settings):
    session_factory = create_session_factory(settings.database.url)
    cloud = YandexDiskService(settings)
    image_editor = ImageEditorImpl(settings.path_to_folder_for_save_image)
    email_sender = EmailSenderImpl(settings)

    app.dependency_overrides.update(
        {
            provide_sqlalchemy_session_stub: session_factory,
            provide_cloud_service_stub: lambda: cloud,
            provide_settings_stub: lambda: settings,
            provide_image_editor_stub: lambda: image_editor,
            provide_email_sender_stub: lambda: email_sender,
        }
    )
    handlers = {
        provide_product_create_handler_stub: provide_product_create_handler,
        provide_product_add_image_handler_stub: provide_product_add_image_handler,  # noqa
        provide_product_get_all_handler_stub: provide_product_get_all_handler,
        provide_product_get_handler_stub: provide_product_get_handler,
        provide_product_get_by_filters_handler_stub: provide_product_get_by_filters_handler,  # noqa
        provide_article_create_handler_stub: provide_article_create_handler,
        provide_article_get_all_handler_stub: provide_article_get_all_handler,
        provide_article_get_handler_stub: provide_article_get_handler,
        provide_image_get_handler_stub: provide_image_get_handler,
        provide_type_solution_create_handler_stub: provide_type_solution_create_handler,  # noqa
        provide_type_solution_get_all_handler_stub: provide_type_solution_get_all_handler,  # noqa
        provide_type_object_create_handler_stub: provide_type_object_create_handler,  # noqa
        provide_type_object_get_all_handler_stub: provide_type_object_get_all_handler,  # noqa
        provide_forwarding_feedback_handler_stub: provide_forwarding_feedback_handler,  # noqa
    }
    app.dependency_overrides.update(handlers)
