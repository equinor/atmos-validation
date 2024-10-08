# Conventions

## Content

- [Dimensions and Coordinates](#1-dimensions-and-coordinate-variables)
  - [Time](#11-time)
  - [Height / Depth](#12-height--depth)
  - [Spatial coordinates](#13-spatial-coordinates)
  - [Longitude / Latitude](#14-latitude-longitude)
- [Data variables](#2-data-variables)
  - [Naming](#21-naming)
  - [Attributes](#22-attributes-for-data-variables)
  - [Measurements](#23-measurments)
  - [Data checks](#24-data-integrity)
- [File attributes](#3-global-attributes)
  - [Common data model](#31-common)
  - [Hindcast data model](#32-hindcast)
  - [Measurment data model](#33-measurement)

## 1 Dimensions and Coordinate Variables

- All dimensions shall be attached to at least one variable
- Dimensions on variables shall match the following naming conventions and sequences:
  - ["south_north", "west_east"]
  - ["Time", "south_north", "west_east"]
  - ["height_[variable_name]", "south_north", "west_east"]
  - ["Time", "height_[variable_name]", "south_north", "west_east"]

### 1.1 Time

- Shall be named exactly "Time"
- Shall not be empty (length > 0)
- Timestamps shall appear in increasing order
- Shall only contain unique values
- The "units" attribute shall be "microseconds since 1900-01-01"
- If source data is a hindcast or single point hindcast, then:
  - The file shall be named according to the time values it contains and contain the length of the time index, in the following format: "datasetName_startTime_endTime_TtimeLenght.nc" with the corresponding time format: "YYYYMMDD". For example, a Nora10 file
  covering the whole year of 1982 and containing 2920 timestamps (a whole year with 3hr resolution) will be named e.g.: "Nora10_19820101_19821231_T2920.nc". Not adhering to startTime and endTime convention would yield a WARNING.
  - Strictly enforced: The files must be named such that they can be sorted in chronological order by timestamp values. For example, naming two files "Nora10_part1.nc" and "Nora10_part2.nc" would yield an error IF part2 contains data for a period before part1. The time-length marker "T[time_length]" is non-optional and not adhering to this convention also yields an error.
- If source data is a measurment, then:
  - the file shall include values for the whole measurment period

### 1.2 Height / Depth

- Shall be named according to the data variable it is attached to. For example, air pressure (with corresponding key "P") will be named: "height_P".
- Depths will still be named "height_XX" but shall be signified by negative values.
- Attribute "units" shall be "m"
- Attribute "CF_standard_name" shall be "height"
- Attribute "long_name" shall be "Height for parameter XX", where XX is e.g. CS, WS, WD etc.

### 1.3 Spatial coordinates

- All data variables shall have "south_north" at the second-to-last index of it's dimensions list, in accordance with the accepted dimensions seen in [Dimensions](#1-dimensions-and-coordinate-variables)
- All data variables shall have "east_west" at the last index of it's dimensions list, in accordance with the accepted dimensions seen in [Dimensions](#1-dimensions-and-coordinate-variables)
- Attribute "units" shall be "degree_north" / "degree_east"
- Attribute "CF_standard_name" shall be "latitude" / "longitude"
- Attribute "long_name" shall be "latitude" / "longitude"

### 1.4 Latitude, Longitude

- Datasets that contains data with spatial coordinates shall contain "LAT" as a coordinate variable
- Datasets that contains data with spatial coordinates shall contain "LON" as a coordinate variable
- "LAT" and "LON" shall be both be defined by dimensions ["south_north", "west_east"]

## 2 Data Variables

### 2.1 Naming

- Shall have valid "key", i.e. be listed in the official database document: [https://atmos.app.radix.equinor.com/config/parameters]

### 2.2 Attributes for data variables

- Shall have attribute "units", "CF_standard_name" and "long_name" with values according to database document.

### 2.3 Measurments

If data source is "measurement", then:

- Shall have attribute "instruments".
- "instruments" shall be a stringified dictionary, i.e. a string that can be evaluated in python as a dictionary, with keys given by "{instrument_type}, {instrument_specification}" to ensure uniqueness. This key shall map to a list of numbers that describe the heights at which the following instrument was being used.
(The reason for using stringified dict is that NetCDF does not allow for objects on attributes. Carrying information over from ASCII files to NetCDF for requires some "nesting" of the information, hence the choice to use a dict with the described keys)
- Example value for key WS (wind speed): '{"PROPELLER ANEMOMETER, some spec": [10.0], "PULSE LIDAR, some spec": [100.0, 150.0, 200.0]}'.
- All instrument types are validated with respect to the "allowed_instruments" entry from the database document.
- Instrument specifications are not validated and can therefore be any string value as long as the keys in the dictionary are unique.

### 2.4 Data integrity

- Shall contain no values outside the range given in the database document by entries "min" and "max". E.g. "AT" (air temperature) shall have values between -50 and 50 degC.

## 3 Global attributes

General instruction: When information is not available "NA" shall be used in place.

### 3.1 Common

The required common attributes can be seen underneath,

```py
# ../atmos_validation/schemas/metadata.py#L20-L30

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
```

*comments*: Any relevant comments related to how the data has been treated shall be provided. It could be basic preprocessing steps etc.

*contractor*: Name of data provider

*classification_level*: Signifies data access according to classification level

*data_type*: If source data is hindcast, single point hindcast, or measurement

*data_history*: Any information about the origin of the data (if not measured directly by the contractor) or changes made to the data (if there has been previous versions of the same data) shall be stated here. If the data has been measured/created directly by the contractor and it is the first version delivered “Original data” shall be stated

*final_reports*:  A list of report file names, separated by comma, shall be provided. All stated report files shall follow the data

*project_name*: Name of the project requesting data

*qc_provider*: Company responsible for the QC. It can be different from the contractor.

where data_type should take either value from the enum:

```py
# ../atmos_validation/schemas/metadata.py#L9-L12

class DataType(str, Enum):
    HINDCAST = "Hindcast"
    MEASUREMENT = "Measurement"
    SP_HINDCAST = "SinglePointHindcast"
```

The data_type value defines secondary requirements on the global attributes on the data file.

The classifcation level should take either value from the enum:

```py
# ../atmos_validation/schemas/classification_level.py#L36-L39

class ClassificationLevel(OrderedEnum):
    OPEN = "Open"
    INTERNAL = "Internal"
    RESTRICTED = "Restricted"
```

### 3.2 Hindcast

Single point hindcast and hindcast both use the hindcast metadata schema.

```py
# ../atmos_validation/schemas/metadata.py#L33-L49

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
```

*calibration*: Indicate whether calibration is applied to he data ‘yes’/ ‘no’

*delivery_date*: Date of the hindcast delivery

*forcing_data*: Data used as the boundary conditions

*memos*: Filenames of memos shall be specified

*model_name*: Name of the model. It shall be unique in the project

*modelling software*: Software and version used in hindcast computation

*nests*: Nests used to create given data

*setup*: Setup storage place in the cold storage. Valid for internal hindcasts only. For external hindcasts ‘NA’ shall be specified

*spatial_resolution*: Spatial resolution in km

*sst_source*:  Source of SST data

*task_manager_external*: Hindcast provider task manager

*task_manager_internal: Equinor task manager handling the project

*time_resolution*: Temporal resolution

### 3.3 Measurement

```py
# ../atmos_validation/schemas/metadata.py#L52-L65

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
```

*asset*: Name of the asset which paid for the data.  In case of sharing data to the third party, permission from the asset is required.

*averaging_period*: Averaging period of measurements in minutes

*country*: Country name on which territory data are acquired. In case of sharing data to the third party, one need obey to country regulation rules related to data sharing.

*data_usability*: Level of the data readiness

*location*: Latitude and longitude of the measurements in degrees (at least three decimals are required after ‘.’)  and corresponding reference datum.  
Format of the location: lat lon, reference

*instrument_specifications*:  Instrument specifications for given measurement locations. Instrument specifications shall be listed in the same order as
the corresponding instrument types.

*installation_types*: Measurement installation type.

*instrument_types*: Types of instruments used for the measurement location.

*mooring_name*: The mooring name shall be unique for each delivered measurement file (across projects, instruments, data deliveries etc) and shall be constructed as follows: project_name + mooring_name + instrument + phase. FOXTROT_MOOR1_GPS_Ph1. Only put single instrumentation in the name in cases where there are multiple instruments.

*total_water_depth*: Total water depth in meters. For wind data total water depth is NA (this parameter is not in the list, it should be included)

*source_file*: A reference to the original data file the NetCDF file was generated from. "NA" can be used if not applicable.

To avoid ambiguous terminology, "data_usability" and "installation_types" are validated against database documents, respectively:

- [https://atmos.app.radix.equinor.com/config/data-usability]
- [https://atmos.app.radix.equinor.com/config/installation-types]

### 3.4 Extras

Extra attributes relevant for the data source can be added using snake_case.
