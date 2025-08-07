from typing import Optional

from pydantic import BaseModel, Field


class WorldPortIndex(BaseModel):
    """World-wide maritime port information."""

    id: float
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
