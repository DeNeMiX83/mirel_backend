from typing import List, Sequence, Union, Tuple
from sqlalchemy import select, Row
from sqlalchemy.orm import joinedload
from .base import Gateway
from mirel.infrastructure.store.sqlalchemy.models import (
    Product as ProductModel,
)
from mirel.core.protocols import ProductGateway
from mirel.core.dto import (
    ProductReturn,
    TypeSolutionReturn,
    TypeObjectReturn,
    ProductGetByFilters,
)
from mirel.core.entities import Product, ProductId


class ProductGatewayImpl(Gateway, ProductGateway):
    async def create(self, product: Product):
        self._session.add(product)
        await self._try_exc_flush()
        return await self.get(product.id)  # type: ignore

    async def get(self, id: ProductId):
        stmt = (
            select(ProductModel)
            .where(Product.id == id)  # type: ignore
            .options(
                joinedload(ProductModel.type_solution),
                joinedload(ProductModel.type_object),
            )
        )
        result = await self._session.execute(stmt)
        product = result.scalars().first()
        return self._product_to_dto(product)

    async def get_all(self) -> List[ProductReturn]:
        stmt = select(ProductModel).options(
            joinedload(ProductModel.type_solution),
            joinedload(ProductModel.type_object),
        )
        result = await self._session.execute(stmt)
        return self._get_products_from_data(result.fetchall())

    async def get_by_filters(
        self, data: ProductGetByFilters
    ) -> List[ProductReturn]:
        stmt = select(ProductModel)
        if data.company is not None:
            stmt = stmt.where(ProductModel.company == data.company)
        if data.year_implementation is not None:
            stmt = stmt.where(
                ProductModel.year_implementation == data.year_implementation
            )
        stmt = stmt.options(
            joinedload(ProductModel.type_solution),
            joinedload(ProductModel.type_object),
        )
        result = await self._session.execute(stmt)

        pre_products = result.fetchall()
        products = list()
        for product in pre_products:
            product_data = product[0]
            if data.type_solution is not None:
                if product_data.type_solution.name == data.type_solution:
                    products.append(product)
                continue
            if data.type_object is not None:
                if product_data.type_object.name == data.type_object:
                    products.append(product)
                continue
            products.append(product)

        return self._get_products_from_data(products)

    def _get_products_from_data(
        self,
        data: Union[
            List[Row[Tuple[ProductModel]]], Sequence[Row[Tuple[ProductModel]]]
        ],
    ) -> List[ProductReturn]:
        products = [
            self._product_to_dto(product) for product in (i[0] for i in data)
        ]
        return products

    def _product_to_dto(self, product):
        if product is None:
            return None
        return ProductReturn(
            id=product.id,
            title=product.title,
            company=product.company,
            type_solution=TypeSolutionReturn(
                id=product.type_solution.id,
                name=product.type_solution.name,
            ),
            type_object=TypeObjectReturn(
                id=product.type_object.id,
                name=product.type_object.name,
            ),
            year_implementation=product.year_implementation,
            preview_description=product.preview_description,
            description=product.description,
            link_to_preview_image=product.link_to_preview_image,
            link_to_image=product.link_to_image,
        )
