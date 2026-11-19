from fastapi import APIRouter, FastAPI, Depends  # pyright: ignore[reportMissingImports]
import os  # pyright: ignore[reportMissingImports]
from helpers.config import get_settings, Settings # pyright: ignore[reportMissingImports]    


base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    
    return {
        "message": f"Welcome to the {app_name}! Version: {app_version}",
        "openai_api_key": app_settings.OPENAI_API_KEY  
        }

