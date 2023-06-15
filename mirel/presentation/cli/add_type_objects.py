import asyncio
from mirel.config import Settings
from mirel.infrastructure.store.sqlalchemy import create_session_factory
from mirel.infrastructure.store.sqlalchemy.models import mapping
from mirel.infrastructure.store.sqlalchemy.gateways import (
    TypeObjectGatewayImpl,
    CommiterImpl,
)
from mirel.core.dto import (
    TypeObjectCreate,
)
from mirel.core.services import TypeObjectService
from mirel.core.handlers import (
    TypeObjectCreateHandler,
)


async def main():
    settings = Settings()
    mapping()
    session_factory = create_session_factory(settings.database.url)
    async for session in session_factory():
        type_object_create_handler = TypeObjectCreateHandler(
            type_object_service=TypeObjectService(),
            type_object_gateway=TypeObjectGatewayImpl(session=session),
            commiter=CommiterImpl(session=session),
        )
        await type_object_create_handler.execute(
            TypeObjectCreate(names=[
                "Производственные, складские",
                "Жильё",
                "Объекты инфраструктуры",
                "Образовательные, учебные",
                "Гостиницы",
                "Транспорт",
                "Спортивные, объекты",
                "Дороги",
                "Торговые, офисные",
                "Культурные, объекты",
                "Медицинские, учреждения",
                "Административные",
            ])
        )

if __name__ == "__main__":
    asyncio.run(main())
