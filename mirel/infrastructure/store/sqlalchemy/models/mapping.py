from .base import Base
from .product import product_mapping
from .type_solution import type_solution_mapping
from .type_object import type_object_mapping
from .company import company_mapping
from .article import article_mapping


def mapping():
    mapper_registry = Base.registry
    product_mapping(mapper_registry)
    type_solution_mapping(mapper_registry)
    type_object_mapping(mapper_registry)
    company_mapping(mapper_registry)
    article_mapping(mapper_registry)
