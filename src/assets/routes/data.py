from urllib import request

from fastapi import APIRouter, FastAPI, Depends, UploadFile, File, status  # pyright: ignore[reportMissingImports]
from fastapi.responses import JSONResponse  # pyright: ignore[reportMissingImports]
import os  # pyright: ignore[reportMissingImports]
from helpers.config import get_settings, Settings # pyright: ignore[reportMissingImports]    
from controllers import DataController, ProcessController  # pyright: ignore[reportMissingImports]
import aiofiles  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
from models import ResponseSignal
import logging
from .schemes.data import ProcessDataRequest  # pyright: ignore[reportMissingImports]   


logging.basicConfig(level=logging.INFO)

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


    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):   
                await f.write(chunk)
    except Exception as e:
        logging.error(f"Error occurred while uploading file: {str(e)}") 
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"Error occurred while uploading file: {str(e)}"}
        )


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={ 
            "signal": ResponseSignal.SUCCESS.value,
            "message": f"File '{file.filename}' uploaded successfully to project '{project_id}'.",
            "data": {"file_path": file_path}
        }
    )

@data_router.post("/process/{project_id}")
async def process_data(project_id: str, request: ProcessDataRequest, 
        data_controller: DataController = Depends(DataController),
        app_settings: Settings = Depends(get_settings)): 

        process_controller = ProcessController(project_id, request.file_id, request.chunk_size, request.overlap_size, request.do_reset)   
        file_content = process_controller.get_file_cotent(request.file_id)
        chunks, file_content_texts, file_content_metadata = process_controller.process_file_content(request.file_id, file_content, request.chunk_size, request.overlap_size)    

        if file_chunks := chunks:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "signal": ResponseSignal.SUCCESS.value,
                    "message": f"File '{request.file_id}' processed successfully for project '{project_id}'.",
                    "data": {
                        "chunks": [chunk.page_content for chunk in file_chunks],
                        "texts": file_content_texts,
                        "metadata": file_content_metadata
                    }
                }
            )   

