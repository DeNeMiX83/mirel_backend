from typing import Callable, AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)


def create_session_factory(
    url: str,
) -> Callable[..., AsyncGenerator[AsyncSession, None]]:
    engine = create_async_engine(url)

    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async def session_factory() -> AsyncGenerator[AsyncSession, None]:
        async with async_session() as session:
            yield session

    return session_factory
