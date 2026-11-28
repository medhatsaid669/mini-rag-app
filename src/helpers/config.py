from pydantic_settings import BaseSettings, SettingsConfigDict  # pyright: ignore[reportMissingImports]

class Settings(BaseSettings):
    APP_NAME: str 
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int
    FILE_DEFAULT_CHUNK_SIZE : int
    UPLOAD_DIRECTORY: str

    MongoDB_URI: str  
    MongoDB_NAME: str 

    class Config:
        env_file = ".env"
       
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    return Settings()   

   
