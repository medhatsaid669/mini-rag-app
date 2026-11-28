from importlib import import_module
from typing import Optional
from wsgiref.validate import validator 
from bson import ObjectId  # pyright: ignore[reportMissingImports]  


try:
	_pydantic = import_module("pydantic")
	BaseModel = _pydantic.BaseModel
	Field = _pydantic.Field
except ModuleNotFoundError:
	class BaseModel:
		def __init__(self, **data):
			self.__dict__.update(data)

	def Field(default=None, **kwargs):
		return default


class DataChunk(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    project_id: str
    chunk_index: int
    content: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
