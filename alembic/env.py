import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Ensure the project's root is in sys.path so imports like "app.db.base" work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# this is the Alembic Config object, which provides access to the .ini file in use
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load environment variables from the .env file
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(basedir, '.env'))

# Pull in the Pydantic‑built URL (which uses DB_HOST, POSTGRES_USER, etc.)
from app.core.config import settings
database_url = settings.SQLALCHEMY_DATABASE_URL
if not database_url:
    raise RuntimeError("settings.SQLALCHEMY_DATABASE_URL is not set")
config.set_main_option("sqlalchemy.url", str(database_url))

# Import Base and register all models so that metadata is populated
from app.db.base import Base, register_models
register_models()

# Point Alembic at your metadata
target_metadata = Base.metadata

# (Optional) Debug print of registered tables
print(f"Registered tables for migration: {list(target_metadata.tables.keys())}")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
