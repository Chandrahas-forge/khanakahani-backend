import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Ensure the project's root is in sys.path so that imports like "app.db.base" work.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load environment variables from the .env file located in the project root.
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), ".env"))

# Override sqlalchemy.url in alembic.ini with the environment variable.
database_url = os.getenv("SQLALCHEMY_DATABASE_URL")
if not database_url:
    raise Exception("SQLALCHEMY_DATABASE_URL not set in .env")
config.set_main_option("sqlalchemy.url", database_url)

# Import Base and register all models
from app.db.base import register_models
target_metadata = register_models()

# Verify models are registered
print(f"Registered models: {[model.__name__ for model in Base.metadata.tables.values()]}")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    
    This configures the context with just a URL and not an Engine.
    """
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
    """Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
