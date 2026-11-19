from fastapi import APIRouter, FastAPI, Depends, UploadFile, File, status  # pyright: ignore[reportMissingImports]
from fastapi.responses import JSONResponse  # pyright: ignore[reportMissingImports]
import os  # pyright: ignore[reportMissingImports]
from helpers.config import get_settings, Settings # pyright: ignore[reportMissingImports]    
from controllers import DataController  # pyright: ignore[reportMissingImports]
import aiofiles 

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile = File(...), 
        data_controller: DataController = Depends(DataController),
        app_settings: Settings = Depends(get_settings)):

# Validate the file properties based on the settings
    is_valid, message = data_controller.validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": message}
        )
    
    # Save the file to the specified directory
    upload_dir = os.path.join(app_settings.UPLOAD_DIRECTORY, project_id)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "File uploaded successfully.", "file_path": file_path}
    )  

    project_dir_path = ProjectController().get_project_path(project_id) 
    file_path = os.path.join(project_dir_path, file.filename)   
