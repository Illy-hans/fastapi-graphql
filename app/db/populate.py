import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models import User, Interest
from datetime import datetime

# Adds development data

async def populate_users_and_interests(session: AsyncSession):
    # Create users
    users = [
        User(name="Robin", email="1@mail.com", password="password1", balance=100.0),
        User(name="Ruby", email="ruby@mail.com", password="password2", balance=150.0),
        User(name="Idman", email="idman@mail.com",  password="password3", balance=200.0),
    ]

    # Create interests
    interests = [
        Interest(name="VIP plan", percentage=7.0, date_added=datetime(2022, 1, 1), date_archived=None, active=True),
        Interest(name="New offer ", percentage=3.5, date_added=datetime(2022, 2, 1), date_archived=None, active=True),
        Interest(name="Legacy", percentage=5, date_added=datetime(2022, 3, 1), date_archived=None, active=True),
    ]

# Add users and interests to the session
    users[0].interests.append(interests[0])
    users[1].interests.append(interests[1])
    users[2].interests.append(interests[2])
    users[3].interests.append(interests[2])
    users[4].interests.append(interests[1])

    session.add_all(users + interests)
    await session.commit()


async def main():
    async with get_session() as session:
        await populate_users_and_interests(session)
        print("Users and interests populated successfully.")

if __name__ == "__main__":
    asyncio.run(main())