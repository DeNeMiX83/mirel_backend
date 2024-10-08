from typing import List, Optional
from sqlalchemy import select
from .base import Gateway
from mirel.core.protocols import TypeObjectGateway
from mirel.core.entities import TypeObject


class TypeObjectGatewayImpl(Gateway, TypeObjectGateway):
    async def create(self, type_object: TypeObject):
        self._session.add(type_object)
        await self._try_exc_flush()

    async def get_by_name(self, name: str) -> Optional[TypeObject]:
        stmt = select(TypeObject).where(TypeObject.name == name)  # type: ignore # noqa
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_all(self) -> List[TypeObject]:
        stmt = select(TypeObject)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
