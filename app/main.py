from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, recipes, users

def create_app() -> FastAPI:
    app = FastAPI(
        title="Khana Kahani API",
        description="Recipe Management System API"
    )


    # Include routers with prefixes
    app.include_router(auth.router, prefix="/auth")
    app.include_router(recipes.router, prefix="/recipes")
    app.include_router(users.router, prefix="/users")

    return app

app = create_app()

