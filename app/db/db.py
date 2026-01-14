from functools import lru_cache
import psycopg
from psycopg_pool import ConnectionPool, AsyncConnectionPool

from app.core.config import settings

DB_URL = settings.DATABASE_URL

@lru_cache
def get_pool(): # sync blocking
    return ConnectionPool(DB_URL, min_size=1, max_size=20, timeout=30, open=False)

@lru_cache
def get_async_pool():
    return AsyncConnectionPool(DB_URL, min_size=1, max_size=20, timeout=30, open=False)

def get_sync_conn():
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;")
        yield conn

async def get_async_conn():
    async with get_async_pool().connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;")
        yield conn