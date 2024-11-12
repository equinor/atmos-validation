import urllib.request
from typing import List

import xarray as xr
from pydantic import TypeAdapter

from ...schemas import (
    ClassificationLevel,
    HindcastMetadata,
    InstallationType,
    InstallationTypes,
    MeasurementMetadata,
)
from ...schemas.data_usability_level import DataUsabilityLevel
from ...schemas.data_usability_levels import DataUsabilityLevels
from ...schemas.metadata import DataType
from ..utils import Severity, is_measurement, validation_node
from ..validation_logger import log

VALID_FINAL_REPORT_EXTENSIONS = ["docx", "pdf", "ppt", "pptx"]


@validation_node(severity=Severity.ERROR)
def file_attributes_validator(ds: xr.Dataset):
    """Validates all requirements on global attributes:"""
    log.debug("Launch root validator")
    return (
        []
        + required_global_attributes_validator(ds)
        + blacklisted_global_attributes_validator(ds)
        + data_type_validator(ds)
        + installation_type_validator(ds)
        + data_usability_validator(ds)
        + classification_level_validator(ds)
        + final_reports_validator(ds)
    )


@validation_node(severity=Severity.ERROR)
def required_global_attributes_validator(ds: xr.Dataset):
    """Validates that all required global attributes are present"""
    if is_measurement(ds):
        data_model = MeasurementMetadata
        extra_requireds = ["country"]
    else:
        data_model = HindcastMetadata
        extra_requireds = []
    result = []
    for attribute in data_model.schema()["required"] + extra_requireds:
        try:
            ds.attrs[attribute]
        except KeyError:
            result += [f"""File attribute "{attribute}" does not exist on dataset"""]
    return result


@validation_node(severity=Severity.ERROR)
def blacklisted_global_attributes_validator(ds: xr.Dataset):
    """
    Validates that unique attributes for measurements are not present on hindcasts
    and vice versa.
    """
    data_type = ds.attrs["data_type"]
    if is_measurement(ds):
        blacklisted_attributes = HindcastMetadata.schema()["required"]
        required_attributes = MeasurementMetadata.schema()["required"]
    else:
        blacklisted_attributes = MeasurementMetadata.schema()["required"]
        required_attributes = HindcastMetadata.schema()["required"]

    result = []
    for attribute in blacklisted_attributes:
        if attribute not in required_attributes:
            try:
                ds.attrs[attribute]  # pylint: disable=pointless-statement
                result += [
                    f"""Attribute "{attribute}" should not exist on a {data_type}"""
                ]
            except KeyError:
                # A KeyError is what we want in this check
                continue

    return result


@validation_node(severity=Severity.ERROR)
def data_type_validator(ds: xr.Dataset):
    """Validates that data_type attribute has correct value"""
    result = []
    try:
        data_type = ds.attrs["data_type"]
        if data_type not in list(DataType):
            result += [
                f"""Global attribute "data_type" must be {DataType.HINDCAST} """
                f"""or {DataType.MEASUREMENT}. Found value: "{data_type}" """
            ]
    except KeyError:
        pass  # missing "data_type" is reported by "required_global_attributes_validator"
    return result


@validation_node(severity=Severity.ERROR)
def final_reports_validator(ds: xr.Dataset):
    """Validates that the final_reports attribute is a list of strings"""
    result = []
    try:
        final_reports = ds.attrs["final_reports"]
        if isinstance(final_reports, list) and all(
            isinstance(item, str) for item in final_reports
        ):
            pass
        elif final_reports == "NA":
            return []
        elif isinstance(final_reports, str):
            final_reports = [rep for rep in final_reports.split(",") if rep]
        else:
            result += [
                'Global attribute "final_reports" is not comma-separated string or string list.'
            ]
            return result
        for item in final_reports:
            file_extension = item.split(".")[-1]
            if file_extension not in VALID_FINAL_REPORT_EXTENSIONS:
                result += [
                    f"File extension for final_reports must be one of {VALID_FINAL_REPORT_EXTENSIONS}"
                ]
    except KeyError:
        pass  # missing "field_reports" is reported by "required_global_attributes_validator"
    except Exception:
        result += ["Could not validate final_reports on global attributes"]
    return result


@validation_node(severity=Severity.ERROR)
def installation_type_validator(ds: xr.Dataset) -> List[str]:
    """Checks that "installation_type" is compliant with the configuration file"""
    result = []
    try:
        valids = load_valid_installation_types()
        installation_type = ds.attrs["installation_type"]
        if installation_type not in valids:
            result += [
                f"""Installation type "{installation_type}" is not in the allowed list. """
                f"""Allowed values: {valids}"""
            ]
    except KeyError:
        pass  # required attributes is validated in 'required_global_attributes_validator'
    except Exception:
        result += ["Could not validate installation_types on global attributes"]
    return result


def load_valid_installation_types() -> List[str]:
    url = "https://atmos.app.radix.equinor.com/config/installation-types"
    log.debug("download installation types")
    with urllib.request.urlopen(url) as response:
        data = response.read()
        parsed_response = InstallationTypes(
            configs=TypeAdapter(List[InstallationType]).validate_json(data)
        ).configs
        return [entry.installation_type for entry in parsed_response]


@validation_node(severity=Severity.ERROR)
def data_usability_validator(ds: xr.Dataset) -> List[str]:
    """Checks that "data_usability" is complient with the configuration file"""
    result = []
    try:
        valids = load_valid_data_usability_levels()
        data_usability_levels: str = ds.attrs["data_usability"]
        # split the string and test each one

        for token in data_usability_levels.split(","):
            data_usability_level = token.strip()
            if data_usability_level not in valids:
                result += [
                    f"""Data usability "{data_usability_level}" is not in the allowed list. """
                    f"""Allowed values: {valids}"""
                ]
    except KeyError:
        pass  # required attributes is validated in 'required_global_attributes_validator'
    except Exception:
        result += ["Could not validate data_usability on global attributes"]
    return result


def load_valid_data_usability_levels() -> List[str]:
    url = "https://atmos.app.radix.equinor.com/config/data-usability"
    log.debug("download data usabilities")
    with urllib.request.urlopen(url) as response:
        data = response.read()
        parsed_response = DataUsabilityLevels(
            configs=TypeAdapter(List[DataUsabilityLevel]).validate_json(data)
        ).configs
        return [entry.level for entry in parsed_response]


@validation_node(severity=Severity.ERROR)
def classification_level_validator(ds: xr.Dataset) -> List[str]:
    """Checks that "classification_level" is compliant with the enum values"""
    result = []
    try:
        classification_level = ds.attrs["classification_level"]
        valids = list(ClassificationLevel)
        if classification_level not in valids:
            result += [
                f"""Classification Level "{classification_level}" is not in the allowed list. """
                f"""Allowed values: {valids}"""
            ]
    except KeyError:
        pass  # required attributes is validated in 'required_global_attributes_validator'
    except Exception:
        result += ["Could not validate classification_level on global attributes"]
    return result
