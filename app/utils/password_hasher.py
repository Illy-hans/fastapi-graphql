from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():

    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(form_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(form_password, hashed_password)

