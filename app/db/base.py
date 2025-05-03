from app.models.base_class import Base

# For Alembic to discover models, import them here
def register_models():
    # Import all models here to register them with Base.metadata
    from app.models.user import User
    from app.models.recipe import Recipe, Favorite, RecipeNote
    
    return Base.metadata

# Call register_models when needed (e.g., in Alembic env.py)