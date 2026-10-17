from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.pantry import PantryItem
from app.schemas.pantry import PantryItemCreate, PantryItemUpdate

async def get_pantry_items(db: AsyncSession, user_id: int) -> list[PantryItem]:
    result = await db.execute(select(PantryItem).where(PantryItem.user_id == user_id))
    return result.scalars().all()

async def add_pantry_item(db: AsyncSession, user_id: int, data: PantryItemCreate) -> PantryItem:
    item = PantryItem(user_id=user_id, **data.model_dump())
    db.add(item)
    await db.flush()
    return item

async def update_pantry_item(db: AsyncSession, user_id: int, item_id: int, data: PantryItemUpdate) -> PantryItem:
    result = await db.execute(
        select(PantryItem).where(PantryItem.id == item_id, PantryItem.user_id == user_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise ValueError("Pantry item not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    await db.flush()
    return item

async def delete_pantry_item(db: AsyncSession, user_id: int, item_id: int) -> None:
    result = await db.execute(
        select(PantryItem).where(PantryItem.id == item_id, PantryItem.user_id == user_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise ValueError("Pantry item not found")
    await db.delete(item)