from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import registry
from .base import Base
from mirel.core.entities import Article as ArticleEntity


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    preview_description = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    link_to_preview_image = Column(String(100), nullable=False, unique=True)
    link_to_image = Column(String(100), nullable=False, unique=True)


def article_mapping(mapper_registry: registry):
    table = Article.__table__
    mapper_registry.map_imperatively(
        ArticleEntity,
        table,
    )
