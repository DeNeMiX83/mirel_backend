from .base import Hаndler
from mirel.core.dto import ImageGet
from mirel.core.protocols import ImageCloudGateway


class ImageGetHandler(Hаndler[ImageGet, str]):
    def __init__(self, image_cloud_gateway: ImageCloudGateway):
        self._image_cloud_gateway = image_cloud_gateway

    async def execute(self, data: ImageGet) -> str:
        image = await self._image_cloud_gateway.get_image(data.filename)
        return image
