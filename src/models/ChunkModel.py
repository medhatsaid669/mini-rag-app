from .BaseDataModel import BaseDataModel    
from .db_schemes import  DataChunk
from .enums.DataBaseEnums import DataBaseEnums
import bson.objectid as objectid  # type: ignore[import-not-found]
from pymongo import ReturnDocument, UpdateResult, DeleteResult, InsertOneResult  # type: ignore[import-not-found]

class ChunkModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client) 
        self.collection_name = DataBaseEnums.CHUNKS.value 

    def create_chunk(self, chunk_data: dict) -> dict:
        """
        Create a new data chunk in the database.

        Args:
            chunk_data (dict): A dictionary containing chunk details.

        Returns:
            dict: The created chunk data.
        """
        # Validate and serialize the chunk data using DataChunkDBScheme
        chunk = DataChunk.DataChunk(**chunk_data)
        serialized_chunk = chunk.dict(by_alias=True)

        # Insert the serialized chunk into the database
        result = self.db_client[self.collection_name].insert_one(serialized_chunk)
        
        # Return the created chunk data with the generated ID
        return {**serialized_chunk, "_id": str(result.inserted_id)}


    def get_chunk(self, project_id: str, page: int = 1, limit: int = 10) -> list:
        """
        Retrieve data chunks associated with a specific project ID.

        Args:
            project_id (str): The ID of the project to retrieve chunks for.
            page (int): The page number to retrieve.
            limit (int): The number of chunks to retrieve per page.

        Returns:
            list: A list of data chunks associated with the specified project ID.
        """
        # Calculate the number of documents to skip based on the page and limit
        skip = (page - 1) * limit
        
        # Query the database for chunks associated with the specified project ID
        chunks_cursor = self.db_client[self.collection_name].find({"project_id": project_id}).skip(skip).limit(limit)
        
        # Convert the cursor to a list of dictionaries and return it
        return [chunk for chunk in chunks_cursor]   


    def insert_chunk(self, chunk_data: dict, batch_size: int = 100) -> list:
        """
        Insert multiple data chunks into the database in batches.

        Args:
            chunk_data (list): A list of dictionaries containing chunk details.
            batch_size (int): The number of chunks to insert in each batch.
        Returns:
            list: A list of the inserted chunk data.
        """
        # Initialize the list to store the inserted chunk data
        inserted_chunks = []

        # Iterate over the chunk data in batches
        for i in range(0, len(chunk_data), batch_size):
            # Get the current batch of chunk data
            batch = chunk_data[i:i + batch_size]

            # Validate and serialize each chunk in the batch
            serialized_chunks = [DataChunk.DataChunk(**chunk).dict(by_alias=True) for chunk in batch]

            # Insert the serialized chunks into the database
            result = self.db_client[self.collection_name].insert_many(serialized_chunks)

            # Add the inserted chunk data to the list
            inserted_chunks.extend([{**chunk, "_id": str(result.inserted_ids[j])} for j, chunk in enumerate(serialized_chunks)])

        return inserted_chunks


    def delete_chunks_by_project_id(self, project_id: str) -> int:
        """
        Delete all data chunks associated with a specific project ID.

        Args:
            project_id (str): The ID of the project to delete chunks for.

        Returns:
            int: The number of deleted chunks.
        """
        # Delete the chunks associated with the specified project ID
        result: DeleteResult = self.db_client[self.collection_name].delete_many({"project_id": project_id})
        
        # Return the number of deleted chunks
        return result.deleted_count 
