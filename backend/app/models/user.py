import enum
from sqlalchemy import String, Integer, Float, Enum, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class GoalEnum(str, enum.Enum):
    weight_loss = "weight_loss"
    muscle_gain = "muscle_gain"
    maintenance = "maintenance"
    general = "general"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sex: Mapped[str | None] = mapped_column(String(10), nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    goal: Mapped[GoalEnum] = mapped_column(Enum(GoalEnum), default=GoalEnum.general)
    calorie_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cultural_preference: Mapped[str | None] = mapped_column(String, nullable=True)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    dietary_flags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)