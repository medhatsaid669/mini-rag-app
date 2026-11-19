from fastapi import APIRouter, FastAPI, Depends, UploadFile, File  # pyright: ignore[reportMissingImports]
import os  # pyright: ignore[reportMissingImports]
from .BaseController import BaseController
from .ProjectController import ProjectController
from models.enums.ResponseEnums import ResponseSignal
from .ProjectController import ProjectController
import re


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # 1 MB in bytes 1024x1024 
        self.upload_directory = self.app_settings.UPLOAD_DIRECTORY

    def validate_uploaded_file(self, file: UploadFile):
        # Validate the file properties based on the settings
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.file_type_supported.value
        if file.size > self.size_scale:
            return False, ResponseSignal.file_size_exceeded.value
        return True, ResponseSignal.file_valid.value
    
    def generate_unique_filename(self, original_filename: str, project_name: str) -> str:
        # Generate a unique filename to avoid overwriting existing files
        random_string = self.generate_random_string(8)
        project_path = ProjectController().get_project_path(project_name)
        unique_filename = f"{random_string}_{original_filename}"    
        cleaned_filename = self.get_cleaned_filename(unique_filename)
        new_file_path = os.path.join(project_path, cleaned_filename)
        while os.path.exists(new_file_path):
            random_string = self.generate_random_string(8)
            unique_filename = f"{random_string}_{original_filename}"
            cleaned_filename = self.get_cleaned_filename(unique_filename)
            new_file_path = os.path.join(project_path, cleaned_filename)
        return new_file_path

    def get_cleaned_filename(self, filename: str) -> str:
        # Clean the filename to remove any unwanted characters
        cleaned_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
        return cleaned_filename 
