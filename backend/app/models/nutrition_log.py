from datetime import datetime, timezone
from sqlalchemy import Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    meal_plan_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("meal_plans.id", ondelete="SET NULL"), nullable=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    protein_g: Mapped[float] = mapped_column(Float, nullable=False)
    carbs_g: Mapped[float] = mapped_column(Float, nullable=False)
    fat_g: Mapped[float] = mapped_column(Float, nullable=False)
    fiber_g: Mapped[float] = mapped_column(Float, nullable=False)
    is_unplanned: Mapped[bool] = mapped_column(Boolean, default=False)