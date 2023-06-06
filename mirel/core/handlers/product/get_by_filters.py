from typing import List
from mirel.core.handlers.base import Hаndler
from mirel.core.protocols import (
    ProductGateway,
)
from mirel.core.dto import ProductGetByFilters
from mirel.core.entities import Product


class ProductGetByFiltersHandler(Hаndler[ProductGetByFilters, None]):
    def __init__(self, product_gateway: ProductGateway):
        self._product_gateway = product_gateway

    async def execute(self, data: ProductGetByFilters) -> List[Product]:
        products = await self._product_gateway.get_by_filters(data)
        return products
