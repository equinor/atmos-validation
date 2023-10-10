from pydantic import BaseModel, Field


class InstallationType(BaseModel):
    installation_type: str
    description: str = Field(default="")
