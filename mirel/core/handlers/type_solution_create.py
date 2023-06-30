from mirel.core.handlers.base import Hаndler
from mirel.core.exceptions import GatewayException, TypeSolutionExistException
from mirel.core.protocols import (
    Commiter,
    # TypeSolutionGateway,
)
from mirel.core.dto import TypeSolutionCreate
from mirel.core.services import TypeSolutionService


class TypeSolutionCreateHandler(Hаndler[TypeSolutionCreate, None]):
    def __init__(
        self,
        type_solution_service: TypeSolutionService,
        type_solution_gateway: TypeSolutionGateway,
        commiter: Commiter,
    ):
        self._type_solution_service = type_solution_service
        self._type_solution_gateway = type_solution_gateway
        self._commiter = commiter

    async def execute(self, data: TypeSolutionCreate) -> None:
        for name in data.names:
            type_solution = self._type_solution_service.create(name=name)
            try:
                await self._type_solution_gateway.create(type_solution)
            except GatewayException:
                ...
        await self._commiter.commit()
