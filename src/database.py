from sqlalchemy import create_engine, text
import os

engine = create_engine(
    f"mssql+pyodbc://{os.environ.get('DB_USERNAME')}:"
    f"{os.environ.get('DB_PASSWORD')}@"
    f"{os.environ.get('DB_HOST')}/"
    f"{os.environ.get('DB_NAME')}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)
"""Engine creation using SQLAlchemy"""


class Database:
    """
    A class to interact with the database, executing SQL queries for various operations related to cardholders, devices, and reservations.
    """

   
    @staticmethod
    def execute_SQL(command_name: str, params: dict = {}, mode: str = 'one'):
        """
        Executes a SQL query based on the provided query key and parameters.
        """
        file_name = './sql/'+ command_name + '.sql'
        file_buffer = open(file_name, 'r', encoding="utf-8")
        sql_statement = file_buffer.read()
        file_buffer.close()
        with engine.connect() as conn:
            result = conn.execute(text(sql_statement), params)
            if mode == 'one':
                return result.fetchone()
            elif mode == 'all':
                return result.fetchall()
            elif mode == 'commit':
                conn.commit()