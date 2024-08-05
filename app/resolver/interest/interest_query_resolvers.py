from sqlalchemy import Result, Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.interest_model import Interest as InterestModel
from app.models.user_interest import UserInterest

async def get_all_interests(session: AsyncSession):
    result: Result[Tuple[InterestModel]]= await session.execute(select(InterestModel))
    interests: Sequence[InterestModel] = result.scalars().all()
    return interests

async def get_interest(session: AsyncSession, interest_id: int):
    stmt = (
        select(InterestModel)
        .where(InterestModel.id == interest_id)
    )
    result = await session.execute(stmt)
    interest: InterestModel | None = result.scalars().first()
    return interest

async def get_active_interest_percentage(session: AsyncSession, user_id: int) -> float:
    stmt = (
        select(UserInterest)
        .where(UserInterest.user_id == user_id)
        .where(UserInterest.active == True)
    )
    result = await session.execute(stmt)
    active_interest: UserInterest | None = result.scalars().first()
    if active_interest is None: 
        print("No active interest found")
        # Returns 0.0 as if there is no active interest there is not one applied to the account
        return 0.0

    latest_interest: int = active_interest.interest_id 
    interest: InterestModel = await get_interest(session, latest_interest)
    return interest.percentage