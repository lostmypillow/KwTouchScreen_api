from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "192.168.2.8"
    DB_NAME: str = "JLL2"
    DB_USERNAME: str = "testsql"
    DB_PASSWORD: str = "test123456"
    SMB_HOST: str = "192.168.2.36"
    SMB_FOLDER: str = "\\kwwebsite\\kwad"
    SMB_USERNAME: str = "exam"
    SMB_PASSWORD: str = "exam"
    # SMB_SERVER=192.168.1.101
    # SMB_FOLDER=\\documents\\test
    # SMB_USERNAME=smbuser
    # SMB_PASSWORD=smbpwd
    DEBUG: bool = True
# TODO replace debug values
settings = Settings()
