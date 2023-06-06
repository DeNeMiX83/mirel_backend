from typing import Optional
from pydantic import BaseModel
from mirel.core.entities import (
    ProductId,
    ArticleId,
    TypeSolutionId,
    TypeObjectId,
)


class ProductCreate(BaseModel):
    title: str
    company: str
    type_solution_id: TypeSolutionId
    type_object_id: TypeObjectId
    year_implementation: int
    preview_description: str
    description: str
    path_to_preview_image: str
    path_to_image: str


class TypeSolutionReturn(BaseModel):
    id: TypeSolutionId
    name: str


class TypeObjectReturn(BaseModel):
    id: TypeObjectId
    name: str


class ProductReturn(BaseModel):
    id: int
    title: str
    company: str
    type_solution: TypeSolutionReturn
    type_object: TypeObjectReturn
    year_implementation: int
    preview_description: str
    description: str
    link_to_preview_image: str
    link_to_image: str


class ProductGet(BaseModel):
    id: ProductId


class ProductGetAll(BaseModel):
    pass


class ProductGetByFilters(BaseModel):
    company: Optional[str]
    type_solution: Optional[str]
    type_object: Optional[str]
    year_implementation: Optional[int]


class ArticleCreate(BaseModel):
    title: str
    preview_description: str
    description: str
    path_to_preview_image: str
    path_to_image: str


class ArticleGet(BaseModel):
    id: ArticleId


class ArticleGetAll(BaseModel):
    pass


class ImageGet(BaseModel):
    filename: str
