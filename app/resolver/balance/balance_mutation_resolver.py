from typing import Optional
from sqlalchemy import Delete, Update, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User as UserModel
from app.models.balance_model import Balance


#ADD MONEY INTO account 