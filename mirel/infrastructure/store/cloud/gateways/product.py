from .base import Gateway
from mirel.core.protocols import ProductCloudGateway


class ProductCloudGatewayImpl(Gateway, ProductCloudGateway):
    async def create_preview_image(self, path_to_file: str) -> str:
        path = await self._service.create_image(path_to_file)
        return path

    async def create_image(self, path_to_file: str) -> str:
        path = await self._service.create_image(path_to_file)
        return path
