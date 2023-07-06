from typing import List, Optional
from sqlalchemy import select
from .base import Gateway
from mirel.core.protocols import TypeSolutionGateway
from mirel.core.entities import TypeSolution


class TypeSolutionGatewayImpl(Gateway, TypeSolutionGateway):
    async def create(self, type_solution: TypeSolution):
        self._session.add(type_solution)
        await self._try_exc_flush()

    async def get_by_name(self, name: str) -> Optional[TypeSolution]:
        stmt = select(TypeSolution).where(TypeSolution.name == name)  # type: ignore # noqa
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_all(self) -> List[TypeSolution]:
        stmt = select(TypeSolution)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
