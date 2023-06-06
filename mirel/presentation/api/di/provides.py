from typing import Callable, Type
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mirel.infrastructure.store.cloud import Service
from mirel.infrastructure.store.sqlalchemy import (
    gateways as sqlalchemy_gateway,
)
from mirel.infrastructure.store.cloud import gateways as cloud_gateway
from mirel.infrastructure.images import ImageEditorImpl
from mirel.core.services import ProductService, ArticleService
from mirel.core.handlers import (
    ProductCreateHandler,
    ProductGetAllHandler,
    ProductGetHandler,
    ProductGetByFiltersHandler,
    TypeSolutionGetAllHandler,
    TypeObjectGetAllHandler,
    ArticleCreateHandler,
    ArticleGetAllHandler,
    ArticleGetHandler,
    ImageGetHandler,
)

from .stubs import (
    provide_sqlalchemy_session_stub,
    provide_cloud_service_stub,
    provide_image_editor_stub,
)


def get_sqlalchemy_gateway(
    gateway_type: Type[sqlalchemy_gateway.Gateway],
) -> Callable[[AsyncSession], sqlalchemy_gateway.Gateway]:
    def _get_gateway(
        session: AsyncSession = Depends(provide_sqlalchemy_session_stub),
    ) -> sqlalchemy_gateway.Gateway:
        return gateway_type(session)

    return _get_gateway


def get_cloud_gateway(
    gateway_type: Type[cloud_gateway.Gateway],
) -> Callable[[Service], cloud_gateway.Gateway]:
    def _get_gateway(
        cloud: Service = Depends(provide_cloud_service_stub),
    ) -> cloud_gateway.Gateway:
        return gateway_type(cloud)

    return _get_gateway


# Product


def provide_product_create_handler(
    product_service: ProductService = Depends(),
    product_gateway: sqlalchemy_gateway.ProductGatewayImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.ProductGatewayImpl)
    ),
    commiter: sqlalchemy_gateway.CommiterImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.CommiterImpl)
    ),
    product_cloud_gateway: cloud_gateway.ProductCloudGatewayImpl = Depends(
        get_cloud_gateway(cloud_gateway.ProductCloudGatewayImpl)
    ),
    image_editor: ImageEditorImpl = Depends(provide_image_editor_stub),
) -> ProductCreateHandler:
    return ProductCreateHandler(
        product_service=product_service,
        product_gateway=product_gateway,
        commiter=commiter,
        product_cloud_gateway=product_cloud_gateway,
        image_editor=image_editor,
    )


def provide_product_get_all_handler(
    product_gateway: sqlalchemy_gateway.ProductGatewayImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.ProductGatewayImpl)
    ),
) -> ProductGetAllHandler:
    return ProductGetAllHandler(
        product_gateway=product_gateway,
    )


def provide_product_get_handler(
    product_gateway: sqlalchemy_gateway.ProductGatewayImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.ProductGatewayImpl)
    ),
) -> ProductGetHandler:
    return ProductGetHandler(
        product_gateway=product_gateway,
    )


def provide_product_get_by_filters_handler(
    product_gateway: sqlalchemy_gateway.ProductGatewayImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.ProductGatewayImpl)
    ),
) -> ProductGetByFiltersHandler:
    return ProductGetByFiltersHandler(
        product_gateway=product_gateway,
    )


def provide_type_solution_get_all_handler(
    type_solution_gateway: sqlalchemy_gateway.TypeSolutionGatewayImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.TypeSolutionGatewayImpl)
    ),
) -> TypeSolutionGetAllHandler:
    return TypeSolutionGetAllHandler(
        type_solution_gateway=type_solution_gateway,
    )


def provide_type_object_get_all_handler(
    type_object_gateway: sqlalchemy_gateway.TypeObjectGatewayImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.TypeObjectGatewayImpl)
    ),
) -> TypeObjectGetAllHandler:
    return TypeObjectGetAllHandler(
        type_object_gateway=type_object_gateway,
    )


# Article


def provide_article_create_handler(
    article_service: ArticleService = Depends(),
    article_gateway: sqlalchemy_gateway.ArticleGatewayImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.ArticleGatewayImpl)
    ),
    commiter: sqlalchemy_gateway.CommiterImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.CommiterImpl)
    ),
    article_cloud_gateway: cloud_gateway.ArticleCloudGatewayImpl = Depends(
        get_cloud_gateway(cloud_gateway.ArticleCloudGatewayImpl)
    ),
    image_editor: ImageEditorImpl = Depends(provide_image_editor_stub),
) -> ArticleCreateHandler:
    return ArticleCreateHandler(
        article_service=article_service,
        article_gateway=article_gateway,
        commiter=commiter,
        article_cloud_gateway=article_cloud_gateway,
        image_editor=image_editor,
    )


def provide_article_get_all_handler(
    article_gateway: sqlalchemy_gateway.ArticleGatewayImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.ArticleGatewayImpl)
    ),
) -> ArticleGetAllHandler:
    return ArticleGetAllHandler(
        article_gateway=article_gateway,
    )


def provide_article_get_handler(
    article_gateway: sqlalchemy_gateway.ArticleGatewayImpl = Depends(
        get_sqlalchemy_gateway(sqlalchemy_gateway.ArticleGatewayImpl)
    ),
) -> ArticleGetHandler:
    return ArticleGetHandler(
        article_gateway=article_gateway,
    )


def provide_image_get_handler(
    image_cloud_gateway: cloud_gateway.ImageCloudGatewayImpl = Depends(
        get_cloud_gateway(cloud_gateway.ImageCloudGatewayImpl)
    ),
) -> ImageGetHandler:
    return ImageGetHandler(
        image_cloud_gateway=image_cloud_gateway,
    )
