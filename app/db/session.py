import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config.settings import settings
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    f"postgresql+asyncpg://{settings.USER}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DB}",
    echo=True
)
# print(engine.url)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    # autocommit=False,
    # autoflush=False,
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()
