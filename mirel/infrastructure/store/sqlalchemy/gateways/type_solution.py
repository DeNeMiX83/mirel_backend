from typing import List
from sqlalchemy import select
from .base import Gateway
from mirel.core.protocols import TypeSolutionGateway
from mirel.core.entities import TypeSolution


class TypeSolutionGatewayImpl(Gateway, TypeSolutionGateway):
    async def get_all(self) -> List[TypeSolution]:
        stmt = select(TypeSolution)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
