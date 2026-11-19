from fastapi import APIRouter, FastAPI, Depends, UploadFile, File  # pyright: ignore[reportMissingImports]
import os  # pyright: ignore[reportMissingImports]
from .BaseController import BaseController
from .ProjectController import ProjectController
from models.enums.ResponseEnums import ResponseSignal


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # 1 MB in bytes 1024x1024 


    def validate_uploaded_file(self, file: UploadFile):
        # Validate the file properties based on the settings
        if file.content_type not in self.app_settings.ALLOWED_FILE_TYPES:
            return ResponseSignal.file_type_supported.value, False
        if file.size > self.size_scale:
            return ResponseSignal.file_size_exceeded.value, False
        return ResponseSignal.file_valid.value, True  
    
