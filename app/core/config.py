from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Cart API"
    DATABASE_URL: str = "postgresql://postgres:xeda@localhost:5432/smart_crad"

    class Config:
        env_file = ".env"

settings = Settings()
