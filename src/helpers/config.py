from pydantic_settings import BaseSettings, SettingsConfigDict  # pyright: ignore[reportMissingImports]

class Settings(BaseSettings):
    APP_NAME: str = "My FastAPI App"
    APP_VERSION: str = "0.1.0"
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int

    class Config:
        env_file = ".env"
       

def get_settings() -> Settings:
    return Settings()   
