from typing import Optional

from pydantic import BaseModel, Field, field_validator


class WorldPortIndex(BaseModel):
    """World-wide maritime port information."""

    oid: float
    world_port_index_number: float
    region_name: str
    main_port_name: str
    alternate_port_name: Optional[str] = Field(default=None)
    unlocode: Optional[str] = Field(default=None)
    country_code: str
    world_water_body: str
    tidal_range: float
    entrance_width: float
    channel_depth: float
    anchorage_depth: float
    cargo_pier_depth: float
    oil_terminal_depth: float
    liquified_natural_gas_terminal_depth: float
    maximum_vessel_length: float
    maximum_vessel_beam: float
    maximum_vessel_draft: float
    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, lat):
        if not (-90 <= lat <= 90):
            raise ValueError(f"Invalid latitude: {lat}. It must be between -90 and 90.")
        return lat

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, lng):
        if not (-180 <= lng <= 180):
            raise ValueError(
                f"Invalid longitude: {lng}. It must be between -180 and 180."
            )
        return lng
