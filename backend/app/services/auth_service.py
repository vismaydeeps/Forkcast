from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRY_HOURS)
    payload = {
        "sub": str(user_id),   # "sub" is the JWT standard claim for subject
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    return int(payload["sub"])

async def register_user(db: AsyncSession, email: str, password: str, name: str) -> User:
    # Check email not already taken
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none():
        raise ValueError("Email already registered")

    user = User(
        email=email,
        password_hash=hash_password(password),
        name=name,
    )
    db.add(user)
    await db.flush()   # Assigns the ID without committing the transaction
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")
    return user