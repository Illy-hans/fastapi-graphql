from app.models.user_model import User as UserModel
from app.schemas.types_schema import LoginResponse
from app.utils.authentication import Authentication
from sqlalchemy.ext.asyncio import AsyncSession

# User can log-in: token(valid for 30m) and user Name are returned 
async def login_resolver(session: AsyncSession, email: str, password: str) -> LoginResponse:
    user: UserModel | None = await Authentication.authenticate_user(session, email, password)
    if not user:
        raise Exception('Invalid username or password')
    access_token: str = Authentication.create_access_token(data={"user_id": user.id})
    return_response = LoginResponse(
        access_token= access_token,
        user_name=user.name,
    )
    return return_response