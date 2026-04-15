from pydantic import BaseModel, Field, field_validator


class DataUsabilityLevel(BaseModel):
    level: str
    description: str = Field(default="")

    @field_validator("level")
    @classmethod
    def validate_level(cls, level: str) -> str:
        """level should not be empty or contain unnecessary white space"""

        if not level.strip():
            raise ValueError("level should not be empty or contain only white space")
        return level.strip()
