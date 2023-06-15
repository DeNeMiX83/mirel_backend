from mirel.core.handlers.base import Hаndler
from mirel.core.exceptions import GatewayException, TypeObjectExistException
from mirel.core.protocols import (
    Commiter,
    TypeObjectGateway,
)
from mirel.core.dto import TypeObjectCreate
from mirel.core.services import TypeObjectService


class TypeObjectCreateHandler(Hаndler[TypeObjectCreate, None]):
    def __init__(
        self,
        type_object_service: TypeObjectService,
        type_object_gateway: TypeObjectGateway,
        commiter: Commiter,
    ):
        self._type_object_service = type_object_service
        self._type_object_gateway = type_object_gateway
        self._commiter = commiter

    async def execute(self, data: TypeObjectCreate) -> None:
        for name in data.names:
            type_object = self._type_object_service.create(
                name=name
            )
            try:
                await self._type_object_gateway.create(type_object)
            except GatewayException as e:
                raise TypeObjectExistException(str(e))
        await self._commiter.commit()
