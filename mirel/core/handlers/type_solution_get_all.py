from typing import List
from mirel.core.handlers.base import Hаndler
from mirel.core.protocols import (
    TypeSolutionGateway,
)
from mirel.core.dto import TypeSolutionGetAll
from mirel.core.entities import TypeSolution


class TypeSolutionGetAllHandler(
    Hаndler[TypeSolutionGetAll, List[TypeSolution]]
):
    def __init__(self, type_solution_gateway: TypeSolutionGateway):
        self._type_solution_gateway = type_solution_gateway

    async def execute(self, data: TypeSolutionGetAll) -> List[TypeSolution]:
        type_solutions = await self._type_solution_gateway.get_all()
        return type_solutions
