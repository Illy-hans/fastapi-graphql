import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config.settings import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr

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


# async def init_db():
#     from app.models import User, Interest, user_interest
#     print("Starting database initialization...")
#     print(f"User table: {User.__table__}")
#     print(f"Interest table: {Interest.__table__}")
#     print(f"user interest table: {user_interest}")
#     print(Base.metadata.tables)
#     print(f"All tables: {Base.metadata.tables}")
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     print("Database tables created.")

# async def main():
#     await init_db()
#     print("Database initialized.")

# if __name__ == "__main__":
#     asyncio.run(main())

