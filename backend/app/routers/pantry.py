from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.database import get_db
from app.redis_client import get_redis
from app.schemas.pantry import PantryItemCreate, PantryItemUpdate, PantryItemResponse
from app.services import pantry_service, spoonacular_service
from app.middleware.auth_middleware import get_current_user
from app.models.user import User

router = APIRouter(prefix="/pantry", tags=["pantry"])

# Static path — must come before /{item_id} to avoid path-matching conflicts
@router.get("/ingredients/search")
async def search_ingredients(
    query: str,
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
):
    return await spoonacular_service.autocomplete_ingredients(query, redis)

@router.get("", response_model=list[PantryItemResponse])
async def list_pantry(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await pantry_service.get_pantry_items(db, current_user.id)

@router.post("", response_model=PantryItemResponse, status_code=201)
async def create_pantry_item(
    body: PantryItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await pantry_service.add_pantry_item(db, current_user.id, body)

@router.put("/{item_id}", response_model=PantryItemResponse)
async def update_pantry_item(
    item_id: int,
    body: PantryItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await pantry_service.update_pantry_item(db, current_user.id, item_id, body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{item_id}", status_code=204)
async def delete_pantry_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await pantry_service.delete_pantry_item(db, current_user.id, item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))