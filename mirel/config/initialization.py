from contextlib import suppress
from fastapi import Depends
from mirel.config import Settings
from mirel.core.dto import (
    TypeSolutionCreate,
    TypeObjectCreate,
)
from mirel.core.handlers import (
    TypeObjectCreateHandler,
    TypeSolutionCreateHandler,
)
from mirel.presentation.api.di.stubs import (
    provide_type_object_create_handler_stub
) 


async def initial_initialization(
    settings: Settings, 
    type_object_create_handler: TypeObjectCreateHandler = Depends(provide_type_object_create_handler_stub)
):
    await type_object_create_handler.execute(
        TypeObjectCreate(name='Тест')
    )
