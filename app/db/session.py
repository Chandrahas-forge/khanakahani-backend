from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URL),  # convert to string hereURL,
    echo=True,
    future=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)