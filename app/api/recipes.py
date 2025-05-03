from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.api.deps import get_db, get_current_user
from app.models.recipe import Recipe
from app.crud import crud_recipe
from app.schemas.recipe import RecipeCreate, RecipeOut
from app.schemas.recipe import RecipeNoteCreate, RecipeNoteOut

router = APIRouter(
    tags=["Recipes"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=RecipeOut, status_code=status.HTTP_201_CREATED)
def create_new_recipe(
    recipe_in: RecipeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud_recipe.create_recipe(db, recipe_in, owner_id=current_user.id)

@router.get("/", response_model=List[RecipeOut])
def list_recipes(
    cuisine: Optional[str] = Query(None),
    ingredients: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(Recipe).filter(Recipe.owner_id == current_user.id)
    if cuisine:
        query = query.filter(Recipe.cuisine.ilike(f"%{cuisine}%"))
    if ingredients:
        query = query.filter(Recipe.ingredients.ilike(f"%{ingredients}%"))
    if tags:
        query = query.filter(Recipe.tags.ilike(f"%{tags}%"))
    recipes = query.offset((page - 1) * limit).limit(limit).all()
    return recipes

@router.get("/{recipe_id}", response_model=RecipeOut)
def read_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=RecipeOut)
def replace_recipe(
    recipe_id: int,
    recipe_in: RecipeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return crud_recipe.update_recipe(db, recipe, recipe_in)

@router.patch("/{recipe_id}", response_model=RecipeOut)
def partial_update_recipe(
    recipe_id: int,
    update_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return crud_recipe.partial_update_recipe(db, recipe, update_data)

@router.delete("/{recipe_id}", status_code=status.HTTP_200_OK)
def remove_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    crud_recipe.delete_recipe(db, recipe)
    return {"msg": "Recipe deleted successfully"}

@router.post("/{recipe_id}/favorite", status_code=status.HTTP_200_OK)
def mark_favorite(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    favorite = crud_recipe.add_favorite(db, recipe_id, current_user.id)
    return {"msg": "Recipe marked as favorite"} if favorite else HTTPException(status_code=400, detail="Could not mark as favorite")

@router.delete("/{recipe_id}/favorite", status_code=status.HTTP_200_OK)
def remove_favorite(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    favorite = crud_recipe.remove_favorite(db, recipe_id, current_user.id)
    if not favorite:
        raise HTTPException(status_code=400, detail="Recipe was not marked as favorite")
    return {"msg": "Favorite removed"}

@router.post("/{recipe_id}/notes", response_model=RecipeNoteOut, status_code=status.HTTP_201_CREATED)
def add_recipe_note(
    recipe_id: int,
    note_in: RecipeNoteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    note = crud_recipe.add_recipe_note(db, recipe_id, current_user.id, note_in)
    return note

@router.get("/{recipe_id}/notes", response_model=List[RecipeNoteOut])
def list_recipe_notes(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == current_user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    notes = crud_recipe.get_recipe_notes(db, recipe_id)
    return notes