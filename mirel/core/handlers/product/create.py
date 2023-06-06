from mirel.core.handlers.base import Hаndler
from mirel.core.exceptions import UnsupportedImageFormat
from mirel.core.protocols import (
    Commiter,
    ProductGateway,
    ProductCloudGateway,
    ImageEditor,
)
from mirel.core.dto import ProductCreate, ProductReturn
from mirel.core.services import ProductService


class ProductCreateHandler(Hаndler[ProductCreate, ProductReturn]):
    def __init__(
        self,
        product_service: ProductService,
        product_gateway: ProductGateway,
        commiter: Commiter,
        product_cloud_gateway: ProductCloudGateway,
        image_editor: ImageEditor,
    ):
        self._product_service = product_service
        self._product_gateway = product_gateway
        self._commiter = commiter
        self._product_cloud_gateway = product_cloud_gateway
        self._image_editor = image_editor

    async def execute(self, data: ProductCreate) -> ProductReturn:
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
            await self._product_cloud_gateway.create_preview_image(
                data.path_to_preview_image
            )
        )
        link_to_image = await self._product_cloud_gateway.create_image(
            data.path_to_image
        )

        product = self._product_service.create(
            data, link_to_preview_image, link_to_image
        )

        product_return = await self._product_gateway.create(product)
        await self._commiter.commit()
        return product_return
