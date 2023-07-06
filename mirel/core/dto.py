from typing import Optional, List
from pydantic import BaseModel
from mirel.core.entities import (
    ProductId,
    ArticleId,
    TypeSolutionId,
    TypeObjectId,
    CompanyId,
)


class ProductCreate(BaseModel):
    title: str
    company_names: List[str]
    type_solution_names: List[str]
    type_object_names: List[str]
    year_implementation: int
    preview_description: str
    description: List[str]
    path_to_preview_image: str
    path_to_image: str


class ProductAddImage(BaseModel):
    product_id: ProductId
    path_to_image: str


class TypeSolutionReturn(BaseModel):
    id: TypeSolutionId
    name: str


class TypeObjectReturn(BaseModel):
    id: TypeObjectId
    name: str


class CompanyReturn(BaseModel):
    id: CompanyId
    name: str


class ProductReturn(BaseModel):
    id: int
    title: str
    companies: List[CompanyReturn]
    type_solutions: List[TypeSolutionReturn]
    type_objects: List[TypeObjectReturn]
    year_implementation: int
    preview_description: str
    description: List[str]
    link_to_preview_image: str
    links_to_images: List[str]


class ProductGet(BaseModel):
    id: ProductId


class ProductGetAll(BaseModel):
    ...


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
    ...


class TypeSolutionCreate(BaseModel):
    names: List[str]


class TypeSolutionGetAll(BaseModel):
    ...


class TypeObjectCreate(BaseModel):
    names: List[str]


class TypeObjectGetAll(BaseModel):
    ...


class ImageGet(BaseModel):
    filename: str


class ForwardingFeedbackData(BaseModel):
    name: str
    email: str
    telephone: str
    msg: str
    email_recipient: Optional[str] = None
