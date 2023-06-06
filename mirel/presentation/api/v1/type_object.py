from typing import List
from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from mirel.core.dto import (
    TypeObjectGetAll as TypeObjectGetAllForHandler,
)
from mirel.core.entities import TypeObject
from mirel.core.handlers import (
    TypeObjectGetAllHandler,
)
from mirel.presentation.api.di.stubs import (
    provide_type_object_get_all_handler_stub,
)

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[TypeObject],
)
async def get_all_type_object(
    response: Response,
    handler: TypeObjectGetAllHandler = Depends(
        provide_type_object_get_all_handler_stub
    ),
):
    type_objects = await handler.execute(TypeObjectGetAllForHandler())
    return type_objects
