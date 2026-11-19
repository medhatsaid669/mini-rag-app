from fastapi import APIRouter, FastAPI, Depends, UploadFile, File  # pyright: ignore[reportMissingImports]
import os  # pyright: ignore[reportMissingImports]
from helpers.config import get_settings, Settings # pyright: ignore[reportMissingImports]    
from controllers import DataController  # pyright: ignore[reportMissingImports]


data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile = File(...), 
        data_controller: DataController = Depends(DataController),
        app_settings: Settings = Depends(get_settings)):

# Validate the file properties based on the settings
 is_valid, result_signal = data_controller().validate_uploaded_file(file=file)
 return {
    "project_id": project_id,
    "filename": file.filename,
    "content_type": file.content_type,
    "is_valid": is_valid,
    "result_signal": result_signal
 }
