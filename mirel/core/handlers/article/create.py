from mirel.core.handlers.base import Hаndler
from mirel.core.exceptions import UnsupportedImageFormat
from mirel.core.protocols import (
    Commiter,
    ArticleGateway,
    ArticleCloudGateway,
    ImageEditor,
)
from mirel.core.dto import ArticleCreate
from mirel.core.entities import Article
from mirel.core.services import ArticleService


class ArticleCreateHandler(Hаndler[ArticleCreate, Article]):
    def __init__(
        self,
        article_service: ArticleService,
        article_gateway: ArticleGateway,
        commiter: Commiter,
        article_cloud_gateway: ArticleCloudGateway,
        image_editor: ImageEditor,
    ):
        self._article_service = article_service
        self._article_gateway = article_gateway
        self._commiter = commiter
        self._article_cloud_gateway = article_cloud_gateway
        self._image_editor = image_editor

    async def execute(self, data: ArticleCreate) -> Article:
        allowed_formats = ["png", "jpg", "jpeg"]
        preview_image_file_ext = data.path_to_preview_image.split(".")[-1]
        image_file_ext = data.path_to_preview_image.split(".")[-1]
        if (
            preview_image_file_ext not in allowed_formats
            or image_file_ext not in allowed_formats
        ):
            raise UnsupportedImageFormat()

        data.path_to_preview_image = await self._image_editor.optimize(
            data.path_to_preview_image
        )
        data.path_to_image = await self._image_editor.optimize(
            data.path_to_image
        )
        link_to_preview_image = (
            await self._article_cloud_gateway.create_preview_image(
                data.path_to_preview_image
            )
        )
        link_to_image = await self._article_cloud_gateway.create_image(
            data.path_to_image
        )

        article = self._article_service.create(
            data, link_to_preview_image, link_to_image
        )

        await self._article_gateway.create(article)
        await self._commiter.commit()
        return article
