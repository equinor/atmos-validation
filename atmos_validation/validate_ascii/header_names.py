from enum import Enum


class Headers(str, Enum):
    CONTRACTOR = "Contractor/Data Responsible"
    FINAL_REPORT = "Final Reports"
    QC = "QC Provider"
    DURATION = "Duration of Data"
    MOORING = "Mooring Name"
    LOCATION = "Location"
    TOTAL_WATER_DEPTH = "TotalWaterDepth"
    INSTRUMENTS = "Type of Instrument"
    DATA_USTABILITY_LEVEL = "Data Usability Level"
    DATA_HISTORY = "Data History"
    PROJECT_NAME = "Project Name"
    AVERAGING_PERIOD = "Averaging Period"
    INSTALLATION_TYPE = "Measurement Installation Type"
    INSTRUMENT_SPEC = "Specification of Instrument"
    COMMENTS = "Comments"
    PARAMETERS = "% Parameters"
    NULL_VALUE = "Missing Data"
