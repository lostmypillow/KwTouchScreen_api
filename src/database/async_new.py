from aioodbc import create_pool
from contextlib import asynccontextmanager
from dotenv import dotenv_values
from fastapi import FastAPI

config = dotenv_values('.env')
pool = None

@asynccontextmanager
async def db_pool_lifespan(app: FastAPI):
global pool
_dsn =
"Driver=ODBC Driver 18 for SQL Server;"
f"Server={config['db_host']},1433;"
f"Database={config['db_use']};"
f"UID={config['db_usr']};"
f"PWD={config['db_pwd']};"
"Trusted_Connection=no;"
pool = await create_pool(dsn=_dsn)
yield
pool.close()
await pool.wait_closed()

async def select_query(stm, cstr=False):
results = []
async with pool.acquire() as conn:
async with conn.cursor() as cur:
await cur.execute(stm)
cols = [c[0] for c in cur.description]
rows = await cur.fetchall()
for row in rows:
results.append({
col : str(row[i]) if cstr else row[i] for i, col in enumerate(cols)
})
return results

async def execute_query(stm: str, params: tuple):
row_count = 0
async with pool.acquire() as conn:
async with conn.cursor() as cur:
await cur.execute(stm, params)
await cur.execute('select @@rowcount')
row_count = await cur.fetchall()
return row_count[0][0]