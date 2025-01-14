from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
import pathlib
import os
from dotenv import load_dotenv

load_dotenv()

connection_url = f"mssql+pyodbc://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URL')}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"


async_engine = create_async_engine(
    connection_url, pool_size=100, max_overflow=0, pool_pre_ping=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def sql_from_file(command_name):
    file_path = os.path.join(pathlib.Path(
        __file__).parent.resolve(), 'sql', command_name + '.sql')
    with open(file_path, 'r', encoding="utf-8") as file_buffer:
        return file_buffer.read()


async def commit_sql(command_name, **kwargs):
    async with async_session() as session:
        sql_command = await sql_from_file(command_name)
        await session.execute(text(sql_command), kwargs)
        await session.commit()


async def fetch_one_sql(command_name, **kwargs):
    async with async_session() as session:
        sql_command = await sql_from_file(command_name)
        result = await session.execute(text(sql_command), kwargs)
        return result.fetchone()


async def fetch_all_sql(command_name, **kwargs):
    async with async_session() as session:
        sql_command = await sql_from_file(command_name)
        result = await session.execute(text(sql_command), kwargs)
        return result.fetchall()
