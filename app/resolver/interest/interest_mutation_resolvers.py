from typing import Optional
from sqlalchemy import Result, Sequence, Tuple, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.interest_model import Interest as InterestModel
from app.schemas.types_schema import InterestInput 

# Adds new interest option
async def add_new_interest(session: AsyncSession, interest: InterestInput):
    stmt = select(InterestModel).where(InterestModel.name == interest.name)
    result = await session.execute(stmt)
    existing_interest = result.scalars().first()
    if existing_interest:
        return "Interest name already in use"
    
    new_interest = InterestModel(
        name=interest.name, percentage=interest.percentage, date_started=interest.date_started,
        date_ended=interest.date_ended, active=interest.active
    )

    session.add(new_interest)
    await session.commit()

    return "Interest added successfully"

# async def activate_interest(session: AsyncSession, interest_id: int):
#     stmt = select(InterestModel).where(InterestModel.id == interest_id)
#     result = await session.execute(stmt)
#     interest_to_activate: InterestModel | None = result.scalars().first()
#     if interest_to_activate is None:
#         return "Interest id not found: interest does not exist"
    
    