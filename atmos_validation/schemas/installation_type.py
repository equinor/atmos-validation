from pydantic import BaseModel, Field, field_validator


class InstallationType(BaseModel):
    installation_type: str
    description: str = Field(default="")

    @field_validator("installation_type")
    @classmethod
    def validate_installation_type(cls, installation_type: str) -> str:
        """installation_type should not be empty or contain unnecessary white space"""

        if not installation_type.strip():
            raise ValueError(
                "installation_type should not be empty or contain only white space"
            )
        return installation_type.strip()
