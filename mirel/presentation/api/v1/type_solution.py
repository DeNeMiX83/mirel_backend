from typing import List
from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from mirel.core.dto import (
    TypeSolutionGetAll as TypeSolutionGetAllForHandler,
)
from mirel.core.entities import TypeSolution
from mirel.core.handlers import (
    TypeSolutionGetAllHandler,
)
from mirel.presentation.api.di.stubs import (
    provide_type_solution_get_all_handler_stub,
)

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[TypeSolution],
)
async def get_all_type_solution(
    response: Response,
    handler: TypeSolutionGetAllHandler = Depends(
        provide_type_solution_get_all_handler_stub
    ),
):
    type_solutions = await handler.execute(TypeSolutionGetAllForHandler())
    return type_solutions
