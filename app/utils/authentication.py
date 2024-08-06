from contextlib import _AsyncGeneratorContextManager
from datetime import datetime, timedelta, timezone
from typing import Literal
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from app.config.settings import settings
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User as UserModel
from sqlalchemy.future import select

from app.utils.password_hasher import Hasher

SECRET_KEY: str = settings.JWT_SECRET
ALGORITHM: str = settings.JWT_ALGORITHM

class Authentication():

    async def authenticate_user(session: AsyncSession, email: str, password: str):
        stmt = (select(UserModel).where(UserModel.email == email))
        result = await session.execute(stmt)
        user: UserModel | None = result.scalars().first()
        if not user or not Hasher.verify_password(password, user.password):
            return False
        return user
    
    def create_access_token(data: dict):
        to_encode: dict = data.copy()
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


