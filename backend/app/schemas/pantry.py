from pydantic import BaseModel

class PantryItemCreate(BaseModel):
    ingredient_name: str
    ingredient_id: int | None = None
    quantity: float
    unit: str

class PantryItemUpdate(BaseModel):
    quantity: float | None = None
    unit: str | None = None
    is_low: bool | None = None

class PantryItemResponse(BaseModel):
    id: int
    ingredient_name: str
    ingredient_id: int | None
    quantity: float
    unit: str
    is_low: bool

    model_config = {"from_attributes": True}