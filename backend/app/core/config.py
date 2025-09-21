from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "SST Platform"
    DEBUG: bool = True
    # SQLite by default for quick hackathon usage. Change to PostgreSQL later.
    DATABASE_URL: str = "sqlite:///./sst_platform.db"
    SECRET_KEY: str = "change_this_secret_in_prod"  # override with env in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
