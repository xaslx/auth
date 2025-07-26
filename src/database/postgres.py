from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.config import PostgresConfig


def new_session_maker(config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    database_uri = f'postgresql+asyncpg://{config.login}:{config.password}@{config.host}:{config.port}/{config.database}'

    engine = create_async_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
    )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)