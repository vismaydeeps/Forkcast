from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24
    OPENAI_API_KEY: str
    SPOONACULAR_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()