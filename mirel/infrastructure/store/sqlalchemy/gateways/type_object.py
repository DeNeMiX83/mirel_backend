from typing import List
from sqlalchemy import select
from .base import Gateway
from mirel.core.protocols import TypeObjectGateway
from mirel.core.entities import TypeObject


class TypeObjectGatewayImpl(Gateway, TypeObjectGateway):
    async def get_all(self) -> List[TypeObject]:
        stmt = select(TypeObject)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())