from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import registry
from .base import Base
from mirel.core.entities import TypeSolution as TypeSolutionEntity


class TypeSolution(Base):
    __tablename__ = "type_solution"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)


def type_solution_mapping(mapper_registry: registry):
    table = TypeSolution.__table__
    mapper_registry.map_imperatively(
        TypeSolutionEntity,
        table,
    )
