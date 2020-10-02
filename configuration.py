# https://fastapi.tiangolo.com/advanced/settings/

import os

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = "1839afa8d5e4210d117ba3c8ec32b213f581a22fc792c6be30fb178a5b4e0b60"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEFAULT_SUPERUSER_EMAIL: EmailStr = "super.user@example.com"
    DEFAULT_SUPERUSER_FULL_NAME: str = "Super User"
    DEFAULT_SUPERUSER_PASSWORD: str = "passw0rd"
    ENV: str = os.environ["ENV"]
    if ENV == "PROD":
        SQLLITE_DATABASE_URL = "sqlite:////tmp/fastapi_app.db"
    elif ENV == "TEST":
        SQLLITE_DATABASE_URL = "sqlite:///fastapi_app_test.db"
    else:
        SQLLITE_DATABASE_URL = "sqlite:///fastapi_app.db"

    # local MS SQL Server URL
    SQLSERVER_DATABASE_URL = "mssql+pyodbc://(localdb)\MSSQLLocalDB/fastapi_app?driver=SQL+Server+Native+Client+11.0"


# Global settings for the app
settings = Settings()
