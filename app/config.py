from pydantic import BaseSettings

class envValues(BaseSettings):
    DB_HOSTNAME: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_NAME: str
    DB_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


ENV_VALS = envValues()