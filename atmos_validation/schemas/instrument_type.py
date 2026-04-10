from pydantic import BaseModel, Field, field_validator


class InstrumentType(BaseModel):
    instrument_type: str
    description: str = Field(default="")

    @field_validator("instrument_type")
    @classmethod
    def validate_instrument_type(cls, instrument_type: str) -> str:
        """instrument_type should not be empty or contain unnecessary white space"""

        if not instrument_type.strip():
            raise ValueError(
                "instrument_type should not be empty or contain only white space"
            )
        return instrument_type.strip()
