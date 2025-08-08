from __future__ import with_statement

import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.db.base import Base
from app.models import user  # noqa: F401 ensure model is imported

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url() -> str:
    # Alembic supports reading url from env var through ini interpolation
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def run_with_async_connection() -> None:
        async with connectable.connect() as connection:  # type: ignore[attr-defined]
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_with_async_connection())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()