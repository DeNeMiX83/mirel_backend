from mirel.core.handlers.base import Hаndler
from mirel.core.exceptions import (
    UnsupportedImageFormat,
)
from mirel.core.protocols import (
    Commiter,
    ProductGateway,
    ProductCloudGateway,
    ImageEditor,
)
from mirel.core.dto import ProductAddImage


class ProductAddImageHandler(Hаndler[ProductAddImage, None]):
    def __init__(
        self,
        product_gateway: ProductGateway,
        commiter: Commiter,
        product_cloud_gateway: ProductCloudGateway,
        image_editor: ImageEditor,
    ):
        self._product_gateway = product_gateway
        self._commiter = commiter
        self._product_cloud_gateway = product_cloud_gateway
        self._image_editor = image_editor

    async def execute(self, data: ProductAddImage) -> None:
        allowed_formats = ["png", "jpg", "jpeg"]
        image_file_ext = data.path_to_image.split(".")[-1]
        if image_file_ext not in allowed_formats:
            raise UnsupportedImageFormat()

        link_to_image = await self._get_link_to_image(data.path_to_image)

        await self._product_gateway.add_image(
            product_id=data.product_id, link_to_image=link_to_image
        )
        await self._commiter.commit()

    async def _get_link_to_image(self, path_to_image: str):
        path_to_image = await self._image_editor.optimize(path_to_image)
        link_to_image = await self._product_cloud_gateway.create_image(
            path_to_image
        )
        return link_to_image
