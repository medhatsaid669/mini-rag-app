from typing import Optional

from bson import ObjectId  # pyright: ignore[reportMissingImports]
from pydantic import BaseModel, Field  # pyright: ignore[reportMissingImports]

try:
    from pydantic import field_validator  # pyright: ignore[reportMissingImports]
except ImportError:
    from pydantic import validator  # pyright: ignore[reportMissingImports]

    def field_validator(*fields, **kwargs):
        mode = kwargs.pop("mode", None)
        kwargs["pre"] = mode == "before"
        return validator(*fields, **kwargs)


# Define the Project model
class Project(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @field_validator("id", mode="before")
    @classmethod
    def validate_object_id(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        try:
            return str(ObjectId(value))
        except Exception as exc:
            raise ValueError("Invalid ObjectId format") from exc

    # Configuration for the Project model
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

