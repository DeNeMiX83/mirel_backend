from typing import List
from sqlalchemy import select
from .base import Gateway
from mirel.core.protocols import ArticleGateway
from mirel.core.entities import Article, ArticleId


class ArticleGatewayImpl(Gateway, ArticleGateway):
    async def create(self, article: Article):
        self._session.add(article)
        await self._try_exc_flush()

    async def get(self, id: ArticleId):
        stmt = select(Article).where(Article.id == id)  # type: ignore
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_all(self) -> List[Article]:
        stmt = select(Article)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
