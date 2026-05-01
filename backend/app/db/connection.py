import asyncpg
from app.core.config import settings

from typing import Optional, AsyncGenerator

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def create_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=str(settings.database_url),
        min_size=settings.db_min_connections,
        max_size=settings.db_max_connections,
    )


async def init_db():
    global _pool
    if _pool is None:
        try:
            _pool = await create_pool()
            print("Success: Connected to database!")
        except Exception as e:
            print(f"Error: Failed to connect to database: {e}")
            raise e
    else:
        print("Info: DB pool already initialized, skipping.")


async def close_db():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def get_db_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        raise RuntimeError("Error: DB pool not initialized.")
    return _pool


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        yield conn

