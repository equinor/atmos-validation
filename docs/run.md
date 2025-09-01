# Running CLI

## Installation

Prerequisites: Python >=3.8.

Run in your preferred environment:

```pip install atmos_validation```

If using conda, run before the pip install command above:

```conda install git pip```

## Run

After installing, run ```python -m atmos_validation``` to see docstring for available commands and options.

Example usage using the example datasets (need to clone/download repository and run from root for this to work):

- Validating hindcast NetCDF format: ```python -m atmos_validation validate-netcdf examples/hindcast_example```
- Validating measurement NetCDF format: ```python -m atmos_validation validate-netcdf examples/example_netcdf_measurement.nc```
- Validating measurement ascii format: ```python -m atmos_validation validate-ascii examples/example_ascii_measurement.dat```
- Convert an ascii file to NetCDF: ```python -m atmos_validation convert-ascii examples/example_ascii_measurement.dat```

All commands can be run without arguments to trigger docstring output to list args and options documentation.
