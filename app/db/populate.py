import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models import User, Interest
from datetime import datetime

from app.models.balance_model import Balance

# Adds development data

async def populate_users_and_interests(session: AsyncSession):
    # Create users
    users = [
        User(name="Robin", email="1@mail.com", password="password1"),
        User(name="Ruby", email="ruby@mail.com", password="password2"),
        User(name="Idman", email="idman@mail.com",  password="password3"),
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
    users[0].interests.append(interests[2])
    users[1].interests.append(interests[1])

    session.add_all(users + interests)
    await session.flush()

    balances = [
            Balance(user_id=users[0].id, date=datetime(2024, 1, 8), total_balance=100.00, interest_accrued_today=0.0, cumulative_interest_accrued=0.0000),
            Balance(user_id=users[1].id, date=datetime(2024, 1, 8), total_balance=200.00, interest_accrued_today=0.0, cumulative_interest_accrued=0.0000),
            Balance(user_id=users[2].id, date=datetime(2024, 1, 8), total_balance=300.00, interest_accrued_today=0.0, cumulative_interest_accrued=0.0000),
        ]
        
    session.add_all(balances)
    await session.commit()

async def main():
    async with get_session() as session:
        await populate_users_and_interests(session)
        print("Users and interests populated successfully.")

if __name__ == "__main__":
    asyncio.run(main())