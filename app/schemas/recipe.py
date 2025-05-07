from pydantic import BaseModel, conlist
from datetime import datetime
from typing import List

class RecipeBase(BaseModel):
    title: str
    cuisine: str
    ingredients: List[str]  # List of ingredients
    tags: str | None = None
    steps: str


class RecipeCreate(RecipeBase):
    pass

class RecipeOut(RecipeBase):
    id: int
    owner_id: int
    total_favorites: int = 0  # Better name than favorites_count
    is_favorite: bool = False  # Better name than favorited_by_current_user

    class Config:
        orm_mode = True

class RecipeNoteCreate(BaseModel):
    text: str

class RecipeNoteOut(BaseModel):
    id: int
    text: str
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True