from typing import List
from mirel.core.handlers.base import Hаndler
from mirel.core.protocols import (
    ProductGateway,
)
from mirel.core.dto import ProductGetAll
from mirel.core.entities import Product


class ProductGetAllHandler(Hаndler[ProductGetAll, List[Product]]):
    def __init__(self, product_gateway: ProductGateway):
        self._product_gateway = product_gateway

    async def execute(self, data: ProductGetAll) -> List[Product]:
        products = await self._product_gateway.get_all()
        return products
