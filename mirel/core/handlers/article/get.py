from typing import Optional
from mirel.core.handlers.base import Hаndler
from mirel.core.protocols import (
    ArticleGateway,
)
from mirel.core.dto import ArticleGet
from mirel.core.entities import Article


class ArticleGetHandler(Hаndler[ArticleGet, None]):
    def __init__(self, article_gateway: ArticleGateway):
        self._article_gateway = article_gateway

    async def execute(self, data: ArticleGet) -> Optional[Article]:
        article = await self._article_gateway.get(data.id)
        return article
