from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Field

from .classification_level import ClassificationLevel


class DataType(str, Enum):
    HINDCAST = "Hindcast"
    MEASUREMENT = "Measurement"


class CommonMetadata(BaseModel, use_enum_values=True):
    """Common required attributes for all data types"""

    comments: Union[List[str], str]
    contractor: str
    classification_level: ClassificationLevel = Field(
        default=ClassificationLevel.INTERNAL
    )
    data_type: DataType
    data_history: str
    final_reports: List[str]
    project_name: str
    qc_provider: str


class HindcastMetadata(CommonMetadata):
    """Extra global attributes required if data_type == "Hindcast"."""

    calibration: str
    delivery_date: str
    forcing_data: str
    memos: str
    modelling_software: str
    model_name: str
    nests: Union[str, List[str]]
    setup: str
    spatial_resolution: Union[str, List[str]]
    sst_source: str
    task_manager_external: Union[str, List[str]]
    task_manager_internal: Union[str, List[str]]
    time_resolution: str
    topography_source: str


class MeasurementMetadata(CommonMetadata):
    """Extra global attributes required if data_type == "Measurement"."""

    averaging_period: str
    data_usability: str
    instrument_types: str
    instrument_specifications: str
    installation_type: str
    location: Union[str, List[str]]
    mooring_name: str
    source_file: str
    total_water_depth: Union[str, float]
