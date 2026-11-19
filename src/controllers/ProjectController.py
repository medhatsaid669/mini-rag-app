import os
from .BaseController import BaseController
from models.enums.ResponseEnums import ResponseSignal
from fastapi import UploadFile  # pyright: ignore[reportMissingImports] 


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # 1 MB in bytes 1024x1024 

    def get_project_path(self, project_name: str) -> str:
        # Construct the path to the project directory
        project_dir = os.path.join(self.file_dir, project_name)
        
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)  # C   reate the directory if it doesn't exist  

        return project_dir  
