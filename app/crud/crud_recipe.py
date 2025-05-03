from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.recipe import Recipe
from app.models.recipe import RecipeNote
from app.schemas.recipe import RecipeCreate, RecipeNoteCreate, RecipeNoteOut, RecipeOut

def create_recipe(db: Session, recipe_in: RecipeCreate, owner_id: int) -> Recipe:
    recipe = Recipe(**recipe_in.dict(), owner_id=owner_id)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def update_recipe(db: Session, recipe: Recipe, recipe_in: RecipeCreate) -> Recipe:
    for field, value in recipe_in.dict().items():
        setattr(recipe, field, value)
    db.commit()
    db.refresh(recipe)
    return recipe

def partial_update_recipe(db: Session, recipe: Recipe, update_data: dict) -> Recipe:
    for field, value in update_data.items():
        setattr(recipe, field, value)
    db.commit()
    db.refresh(recipe)
    return recipe

def delete_recipe(db: Session, recipe: Recipe):
    db.delete(recipe)
    db.commit()

def add_favorite(db: Session, recipe_id: int, user_id: int):
    # implementation for adding a favorite remains here
    pass

def remove_favorite(db: Session, recipe_id: int, user_id: int):
    # implementation for removing favorite
    pass

def add_recipe_note(db: Session, recipe_id: int, user_id: int, note_in: RecipeNoteCreate):
    note = RecipeNote(
        text=note_in.text,
        recipe_id=recipe_id,
        user_id=user_id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_recipe_notes(db: Session, recipe_id: int):
    return db.query(RecipeNote).filter(RecipeNote.recipe_id == recipe_id).all()