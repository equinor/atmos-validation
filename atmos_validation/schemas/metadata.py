from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from .classification_level import ClassificationLevel


class DataType(str, Enum):
    HINDCAST = "Hindcast"
    MEASUREMENT = "Measurement"
    SP_HINDCAST = "SinglePointHindcast"


class UnprotectedNamespaceModel(BaseModel):
    # to avoid "model_name" warning raised in pydantic V2
    model_config = ConfigDict(protected_namespaces=())


class CommonMetadata(BaseModel, use_enum_values=True):
    """Common required attributes for all data types"""

    comments: Union[List[str], str]
    contractor: str
    classification_level: ClassificationLevel = Field(default="Internal")
    data_type: DataType
    data_history: str
    final_reports: List[str]
    project_name: str
    qc_provider: str


class HindcastMetadata(CommonMetadata, UnprotectedNamespaceModel):
    """Extra global attributes required if data_type == "Hindcast" or data_type == "SinglePointHindcast"."""

    calibration: str
    delivery_date: str
    forcing_data: str
    memos: Union[str, List[str]]
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
    """Extra global attributes if data_type == "Measurement"."""

    asset: Optional[str] = Field(default=None)
    averaging_period: str
    country: str = Field(default="NA")
    data_usability: str
    instrument_types: str
    instrument_specifications: str
    installation_type: str
    location: Union[str, List[str]]
    mooring_name: str
    source_file: str
    total_water_depth: Union[str, float]
