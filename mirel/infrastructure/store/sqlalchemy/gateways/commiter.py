from mirel.core.protocols import Commiter
from .base import Gateway


class CommiterImpl(Gateway, Commiter):
    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
