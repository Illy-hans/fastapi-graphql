import asyncio
from app.db.session import engine, Base
from app.models import User, Interest, UserInterest

async def init_db():
    print("Starting database initialization...")
    async with engine.begin() as conn:
        # For development
        # print(Base.metadata.tables)
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")

async def main():
    await init_db()
    print("Database initialized.")

if __name__ == "__main__":
    asyncio.run(main())