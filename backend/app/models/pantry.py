from sqlalchemy import String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class PantryItem(Base):
    __tablename__ = "pantry_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    ingredient_name: Mapped[str] = mapped_column(String, nullable=False)
    ingredient_id: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Spoonacular ID
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    is_low: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="pantry_items")