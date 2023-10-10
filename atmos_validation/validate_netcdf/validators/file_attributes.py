import urllib.request
from typing import List

import xarray as xr
from pydantic import parse_raw_as

from ...schemas import (
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
    )


@validation_node(severity=Severity.ERROR)
def required_global_attributes_validator(ds: xr.Dataset):
    """Validates that all required global attributes are present"""
    data_model = MeasurementMetadata if is_measurement(ds) else HindcastMetadata
    result = []
    for attribute in data_model.schema()["required"]:
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
        if not (
            isinstance(final_reports, list)
            and all(isinstance(item, str) for item in final_reports)
        ):
            final_reports_types = []
            if not isinstance(final_reports, list):
                final_reports_types += type(final_reports).__name__
            else:
                for item in final_reports:
                    final_reports_types += type(item).__name__
            result += [
                f"""Global attribute "final_reports" must be a list of strings. Found types: {final_reports_types}"""
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
            configs=parse_raw_as(List[InstallationType], data)
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
            configs=parse_raw_as(List[DataUsabilityLevel], data)
        ).configs
        return [entry.level for entry in parsed_response]
