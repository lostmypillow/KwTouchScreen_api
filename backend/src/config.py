from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "192.168.2.12"
    DB_USERNAME: str = "mssql"
    DB_PASSWORD: str = "mssql"
#    DB_HOST: str = "192.168.2.8"
#    DB_USERNAME: str = "testsql"
#    DB_PASSWORD: str = "test123456"
    DB_NAME: str = "JLL2"
    SMB_HOST: str = "192.168.2.36"
    SMB_FOLDER: str = "\\kwwebsite\\kwad"
    SMB_USERNAME: str = "exam"
    SMB_PASSWORD: str = "exam"
    DEBUG: bool = False


# TODO replace debug values
settings = Settings()
