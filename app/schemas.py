from typing import Any
from pydantic import BaseModel 

class UploadMetaData(BaseModel):
    rows: int 
    columns: list[str]
    dtypes: dict[str, str]

class StatsResponse(BaseModel):
    stats: dict[str, dict[str, Any]]

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    question: str
    answer: str
    model: str

class HealthResponse(BaseModel):
    status: str = "ok"

