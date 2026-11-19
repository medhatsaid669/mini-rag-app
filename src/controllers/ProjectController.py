import os
from .BaseController import BaseController

__all__ = ["ProjectController"]


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # 1 MB in bytes 1024x1024 

    def get_project_path(self, project_name: str) -> str:
        # Construct the path to the project directory
        project_dir = os.path.join(self.project_dir, project_name)
        return project_dir

        # Initialize the project directory
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)  # Create the directory if it doesn't exist   
        return os.path.join(self.project_dir, project_name)
        
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)  # C   reate the directory if it doesn't exist  

        return project_dir  
