from typing import List
from mirel.core.handlers.base import Hаndler
from mirel.core.protocols import (
    ArticleGateway,
)
from mirel.core.dto import ArticleGetAll
from mirel.core.entities import Article


class ArticleGetAllHandler(Hаndler[ArticleGetAll, None]):
    def __init__(self, article_gateway: ArticleGateway):
        self._article_gateway = article_gateway

    async def execute(self, data: ArticleGetAll) -> List[Article]:
        articles = await self._article_gateway.get_all()
        return articles
