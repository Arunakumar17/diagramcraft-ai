from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from bson import ObjectId


# Pydantic v2 compatible ObjectId type
def validate_object_id(v):
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)]


class DiagramModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    diagram_type: str
    user_prompt: str
    latex_code: str
    pdf_path: Optional[str] = None
    png_path: Optional[str] = None
    svg_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DiagramResponse(BaseModel):
    id: str
    diagram_type: str
    user_prompt: str
    latex_code: str
    pdf_url: Optional[str] = None
    png_url: Optional[str] = None
    svg_url: Optional[str] = None
    created_at: datetime

class GenerateRequest(BaseModel):
    diagram_type: str
    prompt: str
