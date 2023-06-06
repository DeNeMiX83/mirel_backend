from typing import Optional
from mirel.core.handlers.base import Hаndler
from mirel.core.protocols import (
    ProductGateway,
)
from mirel.core.dto import ProductGet
from mirel.core.entities import Product


class ProductGetHandler(Hаndler[ProductGet, None]):
    def __init__(self, product_gateway: ProductGateway):
        self._product_gateway = product_gateway

    async def execute(self, data: ProductGet) -> Optional[Product]:
        product = await self._product_gateway.get(data.id)
        return product
