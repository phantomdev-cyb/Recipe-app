from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Recipe(BaseModel):
  meal_id: Optional[str]
  title: str
  thumbnail: Optional[str]
  ingredients: Optional[str]
  yt_link: Optional[str]
  recipe: str

class savedRecipe(Recipe):
  id: int
  created_at: datetime