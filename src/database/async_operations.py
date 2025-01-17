from sqlalchemy import text
import pathlib
import os
from .async_session import async_session


async def sql_from_file(command_name: str):
    """_summary_

    Parameters
    ----------
    command_name : str
        _description_

    Returns
    -------
    _type_
        _description_
    """
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
        one_result = result.fetchone()
        return one_result


async def fetch_all_sql(command_name, **kwargs):
    async with async_session() as session:
        sql_command = await sql_from_file(command_name)
        result = await session.execute(text(sql_command), kwargs)
        all_results = result.fetchall()
        return all_results

