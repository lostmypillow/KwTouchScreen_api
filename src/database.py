from sqlalchemy import create_engine, text
import os

# Create the engine once at the module level
engine = create_engine(
    f"mssql+pyodbc://{os.environ.get('DB_USERNAME')}:"
    f"{os.environ.get('DB_PASSWORD')}@"
    f"{os.environ.get('DB_HOST')}/"
    f"{os.environ.get('DB_NAME')}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)

def execute_SQL(command_name: str, mode: str, **kwargs):
    file_path = './sql/' + command_name + '.sql'
    with open(file_path, 'r', encoding="utf-8") as file_buffer:
        sql_statement = file_buffer.read()
    
    with engine.connect() as conn:
        result = conn.execute(text(sql_statement), kwargs)
        if mode == 'one':
            return result.fetchone()
        elif mode == 'all':
            return result.fetchall()
        elif mode == 'commit':
            conn.commit()
            return None
        else:
            raise ValueError(f"Invalid mode: {mode}. Must be 'one', 'all', or 'commit'.")