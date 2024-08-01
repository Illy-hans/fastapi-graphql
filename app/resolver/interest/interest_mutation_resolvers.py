from typing import Optional
from sqlalchemy import Result, Sequence, Tuple, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.interest_model import Interest as InterestModel
from app.schemas.types_schema import InterestInput 
from datetime import datetime

# Adds new interest option
async def add_new_interest(session: AsyncSession, interest: InterestInput):
    stmt = select(InterestModel).where(InterestModel.name == interest.name)
    result = await session.execute(stmt)
    existing_interest: InterestModel | None = result.scalars().first()
    if existing_interest:
        return "Interest name already in use"
    
    new_interest = InterestModel(
        name=interest.name, percentage=interest.percentage, active=interest.active, 
        date_archived=interest.date_archived, archived=interest.archived
    )

    session.add(new_interest)
    await session.commit()

    return "Interest added successfully"

# Archives interest 
async def archive_interest(session: AsyncSession, interest_id: int) -> str:
    stmt = select(InterestModel).where(InterestModel.id == interest_id)
    result = await session.execute(stmt)
    existing_interest: InterestModel | None = result.scalars().first()
    if existing_interest is None: 
        return "Interest id not found: interest does not exist"
    
    existing_interest.archived = True 
    existing_interest.date_archived = datetime.now()

    session.add(existing_interest)
    await session.commit()
    
    return "Interest archived successfully"
