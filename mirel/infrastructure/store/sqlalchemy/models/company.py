from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import registry
from .base import Base
from mirel.core.entities import Company as CompanyEntity


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)


def company_mapping(mapper_registry: registry):
    table = Company.__table__
    mapper_registry.map_imperatively(
        CompanyEntity,
        table,
    )
