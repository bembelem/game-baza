from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent.parent / ".env", extra="ignore")

    # dsn = "postgresql+asyncpg://postgres:mypassword@localhost:5432/mydb"
    @property
    def DB_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DB_URL_SYNC(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

settings = Settings() # type: ignore

