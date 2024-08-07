from datetime import datetime, timedelta, timezone
import jwt
from app.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User as UserModel
from sqlalchemy.future import select
from app.resolvers.user.user_query_resolvers import get_user
from app.utils.password_hasher import Hasher

SECRET_KEY: str = settings.JWT_SECRET
ALGORITHM: str = settings.JWT_ALGORITHM

class Authentication():

    # Confirms user password password
    async def authenticate_user(session: AsyncSession, email: str, password: str):
        stmt = (select(UserModel).where(UserModel.email == email))
        result = await session.execute(stmt)
        user: UserModel | None = result.scalars().first()
        if not user or not Hasher.verify_password(password, user.password):
            return False
        return user
    
    # Creates 30m return token
    def create_access_token(data: dict):
        to_encode: dict = data.copy()
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    async def decode_token(session: AsyncSession, token: str):
        try: 
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user_id: int = decoded_token.get("user_id")
        except jwt.PyJWTError as e:
            print(f"JWT error: {e}")
            return "Could not validate token"
        
        if not user_id:
            return "Could not validate token"
        user: UserModel = await get_user(session, user_id)
        if not user:
            return "Could not validate token"
        return user

