import enum
from sqlalchemy import String, Integer, Date, Enum, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class MealSlotEnum(str, enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"

class MealStatusEnum(str, enum.Enum):
    planned = "planned"
    logged = "logged"
    skipped = "skipped"
    deviated = "deviated"

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    meal_slot: Mapped[MealSlotEnum] = mapped_column(Enum(MealSlotEnum), nullable=False)
    recipe_id: Mapped[str | None] = mapped_column(String, nullable=True)
    recipe_name: Mapped[str] = mapped_column(String, nullable=False)
    recipe_data: Mapped[dict] = mapped_column(JSON, nullable=False)  # Full recipe JSON from LLM
    status: Mapped[MealStatusEnum] = mapped_column(Enum(MealStatusEnum), default=MealStatusEnum.planned)