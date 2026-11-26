from pydantic import BaseModel, Field  # type: ignore[reportMissingImports]
from typing import List, Optional



class ProcessDataRequest(BaseModel):
    file_id: str = Field(..., description="The ID of the file to process")
    chunk_size: Optional[int] = Field(1024, description="The size of each chunk to process")
    overlap_size: Optional[int] = Field(0, description="The size of the overlap between chunks")    
    do_reset: Optional[bool] = Field(False, description="Whether to reset the processing state before starting")    


   