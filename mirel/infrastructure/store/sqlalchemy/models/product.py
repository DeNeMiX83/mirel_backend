from sqlalchemy import Column, ForeignKey, String, Integer, Text
from sqlalchemy.orm import registry, relationship
from .base import Base
from mirel.core.entities import Product as ProductEntity


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    company = Column(String(40), nullable=False)
    type_solution_id = Column(
        Integer, ForeignKey("type_solution.id"), nullable=False
    )
    type_solution = relationship(
        "mirel.infrastructure.store.sqlalchemy.models.type_solution"
        + ".TypeSolution"
    )
    type_object_id = Column(
        Integer, ForeignKey("type_object.id"), nullable=False
    )
    type_object = relationship(
        "mirel.infrastructure.store.sqlalchemy.models.type_object.TypeObject"
    )
    year_implementation = Column(Integer, nullable=False)
    preview_description = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    link_to_preview_image = Column(String(200), nullable=False, unique=True)
    link_to_image = Column(String(200), nullable=False, unique=True)


def product_mapping(mapper_registry: registry):
    table = Product.__table__
    mapper_registry.map_imperatively(
        ProductEntity,
        table,
    )
