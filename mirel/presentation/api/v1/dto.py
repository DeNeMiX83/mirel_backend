from typing import List, Generic, TypeVar
from pydantic import BaseModel
from math import ceil
from mirel.core.dto import (
    ProductGetByFilters as ProductGetByFilters_,
)


class ProductCreate(BaseModel):
    title: str
    company: str
    type_solution_id: int
    type_object_id: int
    year_implementation: int
    preview_description: str
    description: str

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


class ArticleCreate(BaseModel):
    title: str
    preview_description: str
    description: str

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


class ForwardingFeedbackData(BaseModel):
    name: str
    email: str
    telephone: str
    msg: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Иванов Иван Иванович",
                "email": "email@gmail.com",
                "telephone": "+79001231212",
                "msg": "Тестовая обратная связь",
            }
        }
