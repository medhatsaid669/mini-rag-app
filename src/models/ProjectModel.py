from .BaseDataModel import BaseDataModel    
from .db_schemes import  project
from .enums.DataBaseEnums import DataBaseEnums


class ProjectModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client) 
        self.collection_name = DataBaseEnums.PROJECTS.value 


    def create_project(self, project_data: dict) -> dict:
        """
        Create a new project in the database.

        Args:
            project_data (dict): A dictionary containing project details.

        Returns:
            dict: The created project data.
        """
        # Validate and serialize the project data using ProjectDBScheme
        project = project.Project(**project_data)
        serialized_project = project.dict(by_alias=True)

        # Insert the serialized project into the database
        result = self.db_client[self.collection_name].insert_one(serialized_project)
        
        # Return the created project data with the generated ID
        return {**serialized_project, "_id": str(result.inserted_id)}   

    def get_project_or_create_one(self, project):
        """
        Retrieve a project from the database or create a new one if it doesn't exist.

        Args:
            project (dict): A dictionary containing project details.

        Returns:
            dict: The retrieved or created project data.
        """
        # Check if the project already exists in the database
        existing_project = self.db_client[self.collection_name].find_one({"name": project["name"]})
        
        if existing_project:
            # If the project exists, return it
            return existing_project
        else:
            # If the project doesn't exist, create a new one
            return self.create_project(project) 



    def get_all_projects(self, page: int = 1, limit: int = 10) -> list:
        """
        Retrieve all projects from the database.

        Args:
            page (int): The page number to retrieve.
            limit (int): The number of projects to retrieve per page.

        Returns:
            list: A list of all project data.
        """
        # Calculate the skip value for pagination
        skip = (page - 1) * limit

        # Fetch all projects from the database with pagination
        projects_cursor = self.db_client[self.collection_name].find().skip(skip).limit(limit)

        # Convert the cursor to a list of dictionaries
        projects = [project for project in projects_cursor]

        return projects


    
    
