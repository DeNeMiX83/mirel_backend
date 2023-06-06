from typing import List
from mirel.core.handlers.base import Hаndler
from mirel.core.protocols import (
    TypeObjectGateway,
)
from mirel.core.dto import TypeObjectGetAll
from mirel.core.entities import TypeObject


class TypeObjectGetAllHandler(
    Hаndler[TypeObjectGetAll, List[TypeObject]]
):
    def __init__(self, type_object_gateway: TypeObjectGateway):
        self._type_object_gateway = type_object_gateway

    async def execute(self, data: TypeObjectGetAll) -> List[TypeObject]:
        type_objects = await self._type_object_gateway.get_all()
        return type_objects
