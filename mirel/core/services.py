from typing import List
from mirel.core.dto import ProductCreate, ArticleCreate
from mirel.core.entities import (
    Product as Product,
    Article,
    TypeObject,
    TypeSolution,
)


class ProductService:
    def create(
        self,
        data: ProductCreate,
        link_to_preview_image: str,
        link_to_image: str,
        companies: list,
        type_soluions: List,
        type_objects: List,
    ) -> Product:
        return Product(
            id=None,
            title=data.title,
            companies=companies,
            type_solutions=type_soluions,
            type_objects=type_objects,
            year_implementation=data.year_implementation,
            preview_description=data.preview_description,
            description=data.description,
            link_to_preview_image=link_to_preview_image,
            links_to_images=[link_to_image],
        )


class ArticleService:
    def create(
        self,
        data: ArticleCreate,
        link_to_preview_image: str,
        link_to_image: str,
    ) -> Article:
        return Article(
            id=None,
            title=data.title,
            preview_description=data.preview_description,
            description=data.description,
            link_to_preview_image=link_to_preview_image,
            link_to_image=link_to_image,
        )


class TypeObjectService:
    def create(
        self,
        name: str,
    ) -> TypeObject:
        return TypeObject(
            id=None,
            name=name,
        )


class TypeSolutionService:
    def create(
        self,
        name: str,
    ) -> TypeSolution:
        return TypeSolution(
            id=None,
            name=name,
        )
