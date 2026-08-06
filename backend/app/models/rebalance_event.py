import enum
from datetime import datetime, timezone
from sqlalchemy import Integer, Float, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class TriggerTypeEnum(str, enum.Enum):
    cheat_meal = "cheat_meal"
    skipped = "skipped"
    manual = "manual"

class RebalanceEvent(Base):
    __tablename__ = "rebalance_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    triggered_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    trigger_type: Mapped[TriggerTypeEnum] = mapped_column(Enum(TriggerTypeEnum), nullable=False)
    delta_calories: Mapped[float] = mapped_column(Float, nullable=False)
    original_plan_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
    adjusted_plan_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
