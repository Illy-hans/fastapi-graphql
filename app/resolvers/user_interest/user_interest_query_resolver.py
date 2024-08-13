from sqlalchemy import Result, Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_interest import UserInterest as UserInterestModel

async def get_all_user_interests(session: AsyncSession, user_id: int):
    stmt = (select(UserInterestModel).where(UserInterestModel.user_id == user_id))
    result: Result[Tuple[UserInterestModel]] = await session.execute(stmt)
    user_interests: Sequence[UserInterestModel] = result.scalars().all()
    return user_interests

