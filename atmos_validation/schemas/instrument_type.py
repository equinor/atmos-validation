from pydantic import BaseModel, Field


class InstrumentType(BaseModel):
    instrument_type: str
    description: str = Field(default="")
