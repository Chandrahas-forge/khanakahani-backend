from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, recipes, users

def create_app() -> FastAPI:
    app = FastAPI(
        title="Khana Kahani API",
        description="Recipe Management System API"
    )

    # Configure CORS
    origins = [
        "http://localhost:3000",  # React default port
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers with prefixes
    app.include_router(auth.router, prefix="/auth")
    app.include_router(recipes.router, prefix="/recipes")
    app.include_router(users.router, prefix="/users")

    return app

app = create_app()

