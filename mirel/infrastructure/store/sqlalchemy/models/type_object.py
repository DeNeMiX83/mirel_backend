from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import registry
from .base import Base
from mirel.core.entities import TypeObject as TypeObjectEntity


class TypeObject(Base):
    __tablename__ = "type_object"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)


def type_object_mapping(mapper_registry: registry):
    table = TypeObject.__table__
    mapper_registry.map_imperatively(
        TypeObjectEntity,
        table,
    )
