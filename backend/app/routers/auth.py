from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import register_user, authenticate_user, create_access_token
from app.middleware.auth_middleware import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await register_user(db, body.email, body.password, body.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await authenticate_user(db, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    token = create_access_token(user.id)
    return {"access_token": token}

@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user