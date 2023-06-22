import asyncio
from mirel.config import Settings
from mirel.infrastructure.store.sqlalchemy import create_session_factory
from mirel.infrastructure.store.sqlalchemy.models import mapping
from mirel.infrastructure.store.sqlalchemy.gateways import (
    TypeSolutionGatewayImpl,
    CommiterImpl,
)
from mirel.core.dto import (
    TypeSolutionCreate,
)
from mirel.core.services import TypeSolutionService
from mirel.core.handlers import (
    TypeSolutionCreateHandler,
)


async def main():
    settings = Settings()
    mapping()
    session_factory = create_session_factory(settings.database.url)
    async for session in session_factory():
        type_solution_create_handler = TypeSolutionCreateHandler(
            type_solution_service=TypeSolutionService(),
            type_solution_gateway=TypeSolutionGatewayImpl(session=session),
            commiter=CommiterImpl(session=session),
        )
        await type_solution_create_handler.execute(
            TypeSolutionCreate(
                names=[
                    "Проектирование систем электроснабжения до 35 кВ",
                    "Проектирование слаботочных систем, СКС, СКУД",
                    "Автоматизация и диспетчеризация",
                    "Умный дом",
                    "Производство электрощитов, НКУ",
                    "Светотехнические решения",
                    "Электромонтажные работы",
                    "Услуги электролаборатории",
                    "Оборудование 6-35кВ",
                    "Шинопровод",
                    "Источники бесперебойного питания",
                    "Газопоршневые установки",
                    "Поставка оборудования",
                    "Реконструкция внутренней системы освещения",
                    "Зарядные станции для электромобилей",
                    "Архитектурное освещение",
                ]
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
