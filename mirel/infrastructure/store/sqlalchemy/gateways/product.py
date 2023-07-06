from typing import List, Sequence, Union, Tuple
from sqlalchemy import select, Row, insert
from .base import Gateway
from mirel.infrastructure.store.sqlalchemy.models import (
    Product as ProductModel,
    ProductLinkToImage as ProductLinkToImageModel,
    ProductDescription as ProductDescriptionModel,
    link_to_image_association_table,
)
from mirel.core.protocols import ProductGateway
from mirel.core.dto import (
    ProductReturn,
    TypeSolutionReturn,
    TypeObjectReturn,
    ProductGetByFilters,
    CompanyReturn,
)
from mirel.core.entities import Product, ProductId


class ProductGatewayImpl(Gateway, ProductGateway):
    async def create(self, product: Product):
        image = ProductLinkToImageModel(link=product.links_to_images[0])
        self._session.add(image)
        self._session.add(product)
        await self._try_exc_flush()
        stmt = insert(link_to_image_association_table).values(
            link_to_image_id=image.id, product_id=product.id
        )
        await self._session.execute(stmt)
        for description_line_text in product.description:
            description_line = ProductDescriptionModel(
                product_id=product.id, line=description_line_text
            )
            self._session.add(description_line)
        await self._try_exc_flush()
        return await self.get(product.id)  # type: ignore

    async def add_image(
        self, product_id: ProductId, link_to_image: str
    ) -> None:
        image = ProductLinkToImageModel(link=link_to_image)
        self._session.add(image)
        stmt = insert(link_to_image_association_table).values(
            link_to_image_id=image.id, product_id=product_id
        )
        await self._session.execute(stmt)
        await self._try_exc_flush()

    async def get(self, id: ProductId):
        stmt = select(ProductModel).where(Product.id == id)  # type: ignore
        result = await self._session.execute(stmt)
        product = result.scalars().first()
        return self._product_to_dto(product)

    async def get_all(self) -> List[ProductReturn]:
        stmt = select(ProductModel)
        result = await self._session.execute(stmt)
        return self._get_products_from_data(result.unique().fetchall())

    async def get_by_filters(
        self, data: ProductGetByFilters
    ) -> List[ProductReturn]:
        stmt = select(ProductModel)
        if data.year_implementation is not None:
            stmt = stmt.where(
                data.year_implementation == ProductModel.year_implementation
            )
        result = await self._session.execute(stmt)
        pre_products = result.unique().fetchall()
        products = list()
        for product in pre_products:
            product_data = product[0]
            if data.company is not None:
                if data.company in [
                    company.name for company in product_data.companies
                ]:
                    products.append(product)
            if data.type_solution is not None:
                if data.type_solution in [
                    type_solution.name
                    for type_solution in product_data.type_solutions
                ]:
                    products.append(product)
                continue
            if data.type_object is not None:
                if data.type_object in [
                    type_object.name
                    for type_object in product_data.type_objects
                ]:
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
            companies=[
                CompanyReturn(
                    id=company.id,
                    name=company.name,
                )
                for company in product.companies
            ],
            type_solutions=[
                TypeSolutionReturn(
                    id=type_solution.id,
                    name=type_solution.name,
                )
                for type_solution in product.type_solutions
            ],
            type_objects=[
                TypeObjectReturn(
                    id=type_object.id,
                    name=type_object.name,
                )
                for type_object in product.type_objects
            ],
            year_implementation=product.year_implementation,
            preview_description=product.preview_description,
            description=[
                description_line.line
                for description_line in product.description
            ],
            link_to_preview_image=product.link_to_preview_image,
            links_to_images=[
                link_to_image.link for link_to_image in product.links_to_images
            ],
        )
