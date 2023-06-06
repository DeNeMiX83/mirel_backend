from typing import Any
from pydantic.fields import Undefined
from mirel.core.dto import (
    ProductCreate as ProductCreate_,
    ProductGetByFilters as ProductGetByFilters_,
    ArticleCreate as ArticleCreate_,
)


class ProductCreate(ProductCreate_):
    path_to_preview_image: Any = Undefined
    path_to_image: Any = Undefined

    class Config:
        schema_extra = {
            "example": {
                "title": "Пример товара",
                "company": "Примерная компания",
                "type_solution_id": 1,
                "type_object_id": 1,
                "year_implementation": 2022,
                "preview_description": "Примерное описание для предпросмотра",
                "description": "Полное описание товара",
            }
        }
        # exclude = {"created_date"}


class ProductGetByFilters(ProductGetByFilters_):
    ...

    class Config:
        schema_extra = {
            "example": {
                "company": "Тиньк",
                "type_solution": "хз",
                "type_object": "хз",
                "year_implementation": 2023,
            }
        }
        # exclude = {"created_date"}


class ArticleCreate(ArticleCreate_):
    path_to_preview_image: Any = Undefined
    path_to_image: Any = Undefined

    class Config:
        schema_extra = {
            "example": {
                "title": "Пример Статьи",
                "preview_description": "Примерное описание для предпросмотра",
                "description": "Полное описания статьи",
            }
        }
