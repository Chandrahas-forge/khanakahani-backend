from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    cuisine = Column(String, nullable=False)
    # Use ARRAY type for ingredients
    ingredients = Column(ARRAY(String), nullable=False)
    tags = Column(String, nullable=True)
    steps = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", backref="recipes")
    favorites = relationship("Favorite", back_populates="recipe", cascade="all, delete-orphan")
    notes = relationship("RecipeNote", back_populates="recipe", cascade="all, delete-orphan")

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    recipe = relationship("Recipe", back_populates="favorites")
    user = relationship("User", backref="favorites")

class RecipeNote(Base):
    __tablename__ = "recipe_notes"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    recipe = relationship("Recipe", back_populates="notes")
    user = relationship("User", backref="recipe_notes")