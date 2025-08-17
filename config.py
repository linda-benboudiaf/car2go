from typing import List
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    cors_origins: List[str] = ["*"]

    @validator("cors_origins", pre=True)
    def split_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"

settings = Settings()
