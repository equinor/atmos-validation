from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, field_validator

ContractorName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Contractor(BaseModel, extra="forbid"):
    contractor: ContractorName
    divisions: list[ContractorName] | None = Field(
        default=None,
        description="Allowed divisions. Null or an empty list means no divisions are configured.",
    )

    @field_validator("divisions")
    @classmethod
    def validate_unique_divisions(cls, divisions: list[str] | None) -> list[str] | None:
        if divisions is not None and len(divisions) != len(set(divisions)):
            raise ValueError("Division names must be unique within a contractor")
        return divisions


class Contractors(BaseModel):
    configs: list[Contractor]

    @field_validator("configs")
    @classmethod
    def validate_unique_contractors(cls, configs: list[Contractor]) -> list[Contractor]:
        names = [entry.contractor for entry in configs]
        if len(names) != len(set(names)):
            raise ValueError("Contractor names must be unique")
        return configs


def validate_contractor_metadata(
    contractor_names: list[str],
    contractor_divisions: list[str],
    configs: list[Contractor],
) -> list[str]:
    """Validate contractor names and divisions allowed by those contractors."""
    if len(contractor_names) == 1 and contractor_names[0].strip().upper() == "NA":
        contractor_names = []
    configs_by_name = {config.contractor: config for config in configs}
    errors = [
        f'Contractor "{name}" is not in the allowed list.'
        for name in contractor_names
        if name not in configs_by_name
    ]

    allowed_divisions = {
        division
        for name in contractor_names
        if name in configs_by_name
        for division in configs_by_name[name].divisions or []
    }
    for division in contractor_divisions:
        if division not in allowed_divisions:
            errors.append(
                f'Division "{division}" is not allowed for the selected contractors. '
                f"Allowed values: {sorted(allowed_divisions)}"
            )
    return errors
