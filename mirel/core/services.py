from mirel.core.dto import ProductCreate, ArticleCreate
from mirel.core.entities import (
    Product as Product,
    Article,
)


class ProductService:
    def create(
        self,
        data: ProductCreate,
        link_to_preview_image: str,
        link_to_image: str,
    ) -> Product:
        return Product(
            id=None,
            title=data.title,
            company=data.company,
            type_solution_id=data.type_solution_id,
            type_object_id=data.type_object_id,
            year_implementation=data.year_implementation,
            preview_description=data.preview_description,
            description=data.description,
            link_to_preview_image=link_to_preview_image,
            link_to_image=link_to_image,
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
