from .base import Gateway
from mirel.core.protocols import ImageCloudGateway


class ImageCloudGatewayImpl(Gateway, ImageCloudGateway):
    async def get_image(self, path_to_image: str) -> str:
        image = await self._service.get_image(path_to_image)
        return image
