from helpers.config import  get_settings, Settings  # pyright: ignore[reportMissingImports]


class BaseDataModel:
    def __init__(self, db_client):
        self.db_client = db_client
        self.db = self.db_client.get_database() 
        self.settings = get_settings()  
