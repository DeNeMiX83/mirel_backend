from typing import NewType, Optional, List
from dataclasses import dataclass

ProductId = NewType("ProductId", int)
TypeSolutionId = NewType("TypeSolutionId", int)
TypeObjectId = NewType("TypeObjectId", int)
CompanyId = NewType("CompaneId", int)
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
class Company:
    id: Optional[CompanyId]
    name: str


@dataclass
class Product:
    id: Optional[ProductId]
    title: str
    companies: List[Company]
    type_solutions: List[TypeSolution]
    type_objects: List[TypeObject]
    year_implementation: int
    preview_description: str
    description: List[str]
    link_to_preview_image: str
    links_to_images: List[str]


@dataclass
class Article:
    id: Optional[ArticleId]
    title: str
    preview_description: str
    description: str
    link_to_preview_image: str
    link_to_image: str
