from functools import lru_cache
from psycopg_pool import ConnectionPool, AsyncConnectionPool

from app.core.config import settings

# urls for respective users
DB_URL_RO = settings.DATABASE_URL
DB_URL_RW = settings.DATABASE_URL_RW
DB_URL_AR = settings.DATABASE_URL_AUTHR

@lru_cache
def get_pool_ro():  # sync
    return ConnectionPool(DB_URL_RO, min_size=1, max_size=5, timeout=30, open=False)

@lru_cache
def get_async_pool_ro():
    return AsyncConnectionPool(DB_URL_RO, min_size=1, max_size=10, timeout=30, open=False)

@lru_cache
def get_pool_rw():  # sync
    return ConnectionPool(DB_URL_RW, min_size=1, max_size=5, timeout=30, open=False)

@lru_cache
def get_async_pool_rw():
    return AsyncConnectionPool(DB_URL_RW, min_size=1, max_size=10, timeout=30, open=False)

@lru_cache
def get_async_pool_ar():
    return AsyncConnectionPool(DB_URL_AR, min_size=1, max_size=5, timeout=30, open=False)

# getting sync connection with read only session
def get_sync_conn_ro():
    with get_pool_ro().connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;")
        yield conn

# getting async connection with read only session
async def get_async_conn_ro():
    async with get_async_pool_ro().connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;")
        yield conn

# getting sync connection with read write session
def get_sync_conn_rw():
    with get_pool_rw().connection() as conn:
        yield conn

# getting async connection with read write session
async def get_async_conn_rw():
    async with get_async_pool_rw().connection() as conn:
        yield conn

# getting async connection with user reading for auth
async def get_async_conn_ar():
    async with get_async_pool_ar().connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;")
        yield conn
