from pydantic import BaseModel, Field


class DataUsabilityLevel(BaseModel):
    level: str
    description: str = Field(default="")
