from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from .. import model, schema
from ..database import get_db
from fastapi import Response
from typing import List
import httpx, asyncio

router=APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/get_recipes", response_model=List[schema.Recipe])
async def get_recipes(search_item: str):
  url="https://www.themealdb.com/api/json/v1/1/search.php"
  Params={"s":search_item}
  async with httpx.AsyncClient(params=Params, headers={"user":"my-recipe-app/v1"}) as r:
    response=await r.get(url)
    recipes=response.json()
    results=[]

  if recipes["meals"] is None: return []
  for meal in recipes["meals"]:
    Meal_id= meal["idMeal"]
    Title= meal["strMeal"]
    Thumbnail= meal["strMealThumb"]
    Recipe= meal["strInstructions"]
    Yt_link= meal["strYoutube"]
    ingredients=[]
    measurements=[]
    for n in range(1,21):
      if meal[f"strIngredient{n}"] == '':continue
      ingredients.append(meal[f"strIngredient{n}"])
      if meal[f"strMeasure{n}"] == '': continue
      measurements.append(meal[f"strMeasure{n}"])
    ingredient_lines=[f"{ing}- {measure}" for ing,measure in zip(ingredients,measurements)]
    Ingredients=",".join(ingredient_lines)
    results.append(schema.Recipe(
    meal_id=Meal_id,
    title=Title,
    thumbnail=Thumbnail,
    ingredients=Ingredients,
    yt_link=Yt_link,
    recipe=Recipe,
    ))
  return results

@router.post("/post_recipes", response_model=schema.savedRecipe)
def saved(Recipe: schema.Recipe, db: Session=Depends(get_db)):
  existing_recipe=db.query(model.Favourite).filter(model.Favourite.meal_id == Recipe.meal_id).first()
  if existing_recipe:
    raise HTTPException(status_code=400, detail="Recipe Already Saved.")
  new_recipe=model.Favourite(
    meal_id=Recipe.meal_id,
    title=Recipe.title,
    thumbnail=Recipe.thumbnail,
    ingredients=Recipe.ingredients,
    yt_link=Recipe.yt_link,
    recipe=Recipe.recipe,
  )
  db.add(new_recipe)
  db.commit()
  db.refresh(new_recipe)

  return new_recipe

@router.get("/favourites", response_model=List[schema.savedRecipe])
def get_favs(db: Session=Depends(get_db)):
  Recipes=db.query(model.Favourite).all()

  return Recipes

@router.post("/custom_recipes", response_model=schema.savedRecipe)
def custom_recipes(Recipe: schema.Recipe, db: Session=Depends(get_db)):
  new_recipe=model.Favourite(
    meal_id=Recipe.meal_id,
    title=Recipe.title,
    thumbnail=Recipe.thumbnail,
    ingredients=Recipe.ingredients,
    yt_link=Recipe.yt_link,
    recipe=Recipe.recipe,
    )
  db.add(new_recipe)
  db.commit()
  db.refresh(new_recipe)

  return new_recipe

@router.delete("/favourites/{id}")
def delete(id: int, db: Session=Depends(get_db)):
  if not db.query(model.Favourite).filter(model.Favourite.id==id).first():
    raise HTTPException(status_code=404, detail="Recipe doesn't exist.")
  db.query(model.Favourite).filter(model.Favourite.id==id).delete()
  db.commit()
  return{"message": "recipe deleted."}
