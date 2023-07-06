from typing import List, Optional
from sqlalchemy import select
from .base import Gateway
from mirel.core.protocols import CompanyGateway
from mirel.core.entities import Company


class CompanyGatewayImpl(Gateway, CompanyGateway):
    async def create(self, company: Company):
        self._session.add(company)
        await self._try_exc_flush()

    async def get_by_name(self, name: str) -> Optional[Company]:
        stmt = select(Company).where(Company.name == name)  # type: ignore
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_all(self) -> List[Company]:
        stmt = select(Company)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
