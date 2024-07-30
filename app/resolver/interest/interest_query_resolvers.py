from sqlalchemy import Result, Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.interest_model import Interest as InterestModel

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
    interest = result.scalars().first()
    return interest 