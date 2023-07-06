from sqlalchemy import Table, Column, ForeignKey, String, Integer
from sqlalchemy.orm import registry, relationship
from .base import Base
from mirel.core.entities import (
    Product as ProductEntity,
    TypeObject,
    TypeSolution,
    Company,
)


type_object_association_table = Table(
    "product_type_object",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("type_object_id", Integer, ForeignKey("type_object.id")),
)


type_solution_association_table = Table(
    "product_type_solution",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("type_solution_id", Integer, ForeignKey("type_solution.id")),
)


company_association_table = Table(
    "product_company",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("company_id", Integer, ForeignKey("company.id")),
)

link_to_image_association_table = Table(
    "product_link_to_image",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column(
        "link_to_image_id", Integer, ForeignKey("link_to_image_product.id")
    ),
)


class ProductLinkToImage(Base):
    __tablename__ = "link_to_image_product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(200), nullable=False, unique=True)


class ProductDescription(Base):
    __tablename__ = "product_description"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    line = Column(String(100), nullable=False, unique=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    companies = relationship(
        "mirel.infrastructure.store.sqlalchemy.models.company.Company",
        secondary=company_association_table,
        lazy="joined",
        overlaps="companies",
    )
    type_solutions = relationship(
        "mirel.infrastructure.store.sqlalchemy.models.type_solution"
        + ".TypeSolution",
        secondary=type_solution_association_table,
        lazy="joined",
        overlaps="type_solutions",
    )
    type_objects = relationship(
        "mirel.infrastructure.store.sqlalchemy.models.type_object.TypeObject",
        secondary=type_object_association_table,
        lazy="joined",
        overlaps="type_objects",
    )
    year_implementation = Column(Integer, nullable=False)
    preview_description = Column(String(50), nullable=False)
    description = relationship(
        ProductDescription,
        lazy="joined",
    )
    link_to_preview_image = Column(String(200), nullable=False, unique=True)
    links_to_images = relationship(
        ProductLinkToImage,
        secondary=link_to_image_association_table,
        lazy="joined",
    )


def product_mapping(mapper_registry: registry):
    table = Product.__table__
    mapper_registry.map_imperatively(
        ProductEntity,
        table,
        properties={
            "companies": relationship(
                Company,
                secondary=company_association_table,
                lazy="joined",
            ),
            "type_solutions": relationship(
                TypeSolution,
                secondary=type_solution_association_table,
                lazy="joined",
            ),
            "type_objects": relationship(
                TypeObject,
                secondary=type_object_association_table,
                lazy="joined",
            ),
        },
    )
