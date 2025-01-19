# Using pydantic to perform typecasting, which valid our output datatypes. 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    algorithm: str
    access_token_expires_minutes: int
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()


