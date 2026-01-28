import asyncio
from logging.config import fileConfig

# Import TẤT CẢ entities
from src.entities import *

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from src.entities.base_entity import Base, GUID  # Import GUID ở đây

from alembic import context

# Cấu hình để Alembic biết import GUID
def include_object(object, name, type_, reflected, compare_to):
    """Determine whether an object should be included in the migration."""
    return True

def render_item(type_, obj, autogen_context):
    """Custom renderer for GUID type."""
    if type_ == "type" and isinstance(obj, GUID):
        autogen_context.imports.add("from src.entities.base_entity import GUID")
        return "GUID()"
    return False


import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config.environments import settings
from src.entities import base_entity
from src.database.database import database

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set your database URL
config.set_main_option("sqlalchemy.url", database.DATABASE_URL)

target_metadata = base_entity.Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Thêm import cho GUID
        include_object=include_object,
        render_item=render_item,  # Thêm dòng này
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, include_object=include_object, render_item=render_item)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    
    # Tạo async engine
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()