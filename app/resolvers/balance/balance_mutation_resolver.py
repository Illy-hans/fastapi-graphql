from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User as UserModel
from app.models.balance_model import Balance as BalanceModel
from app.db.session import get_session
from decimal import Decimal

from app.resolvers.interest.interest_query_resolvers import get_active_interest_percentage
from app.resolvers.user.user_query_resolvers import get_all_users

# Add deposit to balance.total_amount for the latest balance record
async def add_deposit_into_account(session: AsyncSession, user_id: int, deposit: float) -> str:
    try: 
        stmt = (select(UserModel)
            .options(selectinload(UserModel.balances))
            .where(UserModel.id == user_id))
        
        result = await session.execute(stmt)
        user: UserModel | None = result.scalars().first()
        if user is None:
            return "User id not found: user does not exist"
        
        # Returns last balance based on date added 
        latest_balance: BalanceModel | None = max(user.balances, key=lambda balance: balance.date, default=None)
        
        if latest_balance is None:
            new_balance: BalanceModel = BalanceModel(user_id=user.id, total_balance=deposit, interest_accrued_today=0.000, 
            cumulative_interest_accrued=0.000)
            session.add(new_balance)
        # Add deposit to the total_balance and convert to Decimal to 
        # match database precision
        else: 
            latest_balance.total_balance += Decimal(deposit)
        
        await session.commit()

        return "Deposit added successfully"

    except SQLAlchemyError as error:
            await session.rollback()
            return f"Error occurred: {error}"


async def calculate_daily_interest_rate(session: AsyncSession, user_id: int) -> float:
        async with get_session() as session:
            interest_percentage: float = await get_active_interest_percentage(session, user_id)
            daily_interest_rate: float = interest_percentage / 365 / 100
            return daily_interest_rate


async def update_user_balance_daily(session: AsyncSession, user_id: int):

    stmt = (select(UserModel)
            .options(selectinload(UserModel.balances))
            .where(UserModel.id == user_id))
        
    result = await session.execute(stmt)
    user: UserModel | None = result.scalars().first()
    if user is None:
        return "User id not found: user does not exist"
        
    latest_balance: BalanceModel | None = max(user.balances, key=lambda balance: balance.date, default=None)
    if latest_balance is None:
        return "No existing balance found for user."

    daily_interest_rate: float = await calculate_daily_interest_rate(session, user_id)

    latest_total_balance: Decimal = Decimal(latest_balance.total_balance)
    interest_accrued_today: Decimal = latest_total_balance * Decimal(daily_interest_rate)

    new_total_balance = latest_total_balance + interest_accrued_today
    new_interest_accrued_today = Decimal(interest_accrued_today)
    new_cumulative_interest_accrued = Decimal(latest_balance.cumulative_interest_accrued + interest_accrued_today)

    new_balance: BalanceModel = BalanceModel(
        user_id=user.id,  
        total_balance=new_total_balance,
        interest_accrued_today=new_interest_accrued_today,
        cumulative_interest_accrued=new_cumulative_interest_accrued
    )
    session.add(new_balance)
    await session.commit()

    return "Daily Balance created"



async def all_daily(session: AsyncSession):

    users: list[UserModel] = await get_all_users(session)

    try:
        for user in users:
            if user.balances is None:
                return f"No existing balance found for user {user.id}"
                
            latest_balance: BalanceModel | None = max(user.balances, key=lambda balance: balance.date, default=None)

            daily_interest_rate: float = await calculate_daily_interest_rate(session, user.id)

            latest_total_balance: Decimal = Decimal(latest_balance.total_balance)
            interest_accrued_today: Decimal = latest_total_balance * Decimal(daily_interest_rate)

            new_total_balance = latest_total_balance + interest_accrued_today
            new_interest_accrued_today = Decimal(interest_accrued_today)
            new_cumulative_interest_accrued = Decimal(latest_balance.cumulative_interest_accrued + interest_accrued_today)

            new_balance: BalanceModel = BalanceModel(
                user_id=user.id,  
                total_balance=new_total_balance,
                interest_accrued_today=new_interest_accrued_today,
                cumulative_interest_accrued=new_cumulative_interest_accrued
            )
            session.add(new_balance)
        
        await session.commit()
        return "All users updated"

    except Exception as error:
        await session.rollback()
        return f"An error occurred: {error}"
