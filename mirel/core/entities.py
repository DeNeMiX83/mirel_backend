from typing import NewType, Optional
from dataclasses import dataclass

ProductId = NewType("ProductId", int)
TypeSolutionId = NewType("TypeSolutionId", int)
TypeObjectId = NewType("TypeObjectId", int)
ArticleId = NewType("ArticleId", int)


@dataclass
class TypeSolution:
    id: Optional[TypeSolutionId]
    name: str


@dataclass
class TypeObject:
    id: Optional[TypeObjectId]
    name: str


@dataclass
class Product:
    id: Optional[ProductId]
    title: str
    company: str
    type_solution_id: TypeSolutionId
    type_object_id: TypeObjectId
    year_implementation: int
    preview_description: str
    description: str
    link_to_preview_image: str
    link_to_image: str


@dataclass
class Article:
    id: Optional[ArticleId]
    title: str
    preview_description: str
    description: str
    link_to_preview_image: str
    link_to_image: str
