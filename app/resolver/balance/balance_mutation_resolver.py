from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User as UserModel
from app.models.balance_model import Balance as BalanceModel
from decimal import Decimal

#Add deposit into balance
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


