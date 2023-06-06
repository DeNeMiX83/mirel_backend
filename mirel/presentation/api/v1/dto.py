from typing import Any, List, Generic, TypeVar
from pydantic import BaseModel
from pydantic.fields import Undefined
from math import ceil
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


ItemsType = TypeVar("ItemsType")


class PaginationResponse(BaseModel, Generic[ItemsType]):
    items: List[ItemsType]
    page: int
    pages: int
    size: int
    total: int

    @staticmethod
    def get_by_items(items: List[ItemsType], page: int, size: int):
        offset_start = page * size
        offset_end = (page + 1) * size
        count_items = len(items)
        pages = ceil(count_items / size)

        return PaginationResponse(
            items=items[offset_start:offset_end],
            page=page,
            pages=pages,
            size=size,
            total=count_items,
        )
