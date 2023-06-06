from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from mirel.core.exceptions import GatewayException


class Gateway:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def _try_exc_flush(self):
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise GatewayException(str(e))
