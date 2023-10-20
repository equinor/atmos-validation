# atmos-validation

[![Build](https://github.com/equinor/atmos-validation/actions/workflows/ci-check-pr.yml/badge.svg)](https://github.com/equinor/atmos-validation/actions/workflows/ci-check-pr.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/licenses/mit)
[![Coverage badge](https://github.com/equinor/atmos-validation/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/equinor/atmos-validation/tree/python-coverage-comment-action-data)

A library containing validation checks to be run on hindcast or measurement data to ensure API compliance and standardization.

Atmos is a project to streamline discoverability and data access for weather data sources through APIs. First step to build a lean and efficient API is converting data to standard format.

## Data Validation

In order to ingest measurement or hindcast data into the Atmos Data Store, every source file needs to pass validation. Validation makes sure that the file is compliant with the data conventions specified in [Conventions](https://github.com/equinor/atmos-validation/blob/main/docs/conventions.md). The standard file formats for source files are NetCDF files for hindcasts and ASCII or NetCDF for measurements.

Measurements by definition contains data for a single geographical location, where as hindcasts are bigger models containing time series for a multitude of locations in (possibly rotated) grids. Measurement files are therefore expected to contain all its data in a single file. A hindcast is comprised of a set of NetCDF files - all with the same coordinates, attributes and variables - where a single file contains data for a unique time period. Depending on the size of the files, the time separation should be either monthly or yearly. A rule-of-thumb is that if file size grows more than 4 GB it should be split into smaller files. See [docs](https://github.com/equinor/atmos-validation/blob/main/docs/conventions.md#11-time) or [example](https://github.com/equinor/atmos-validation/tree/main/examples/hindcast_example) for how to name hindcast files.

To run validation on NetCDF and ASCII source files, we have built the atmos_validation CLI/library. The documentation will describe these checks and the standard format, and how to run validation using the CLI tool.

## Documentation

- [Conventions](https://github.com/equinor/atmos-validation/blob/main/docs/conventions.md)
- [Running CLI](https://github.com/equinor/atmos-validation/blob/main/docs/run.md)

## Examples

- [Hindcast netcdfs format example](https://github.com/equinor/atmos-validation/tree/main/examples/hindcast_example)
- [Measurement netcdf format example](https://github.com/equinor/atmos-validation/blob/main/examples/example_netcdf_measurement.nc)
- [Measurement ascii format example](https://github.com/equinor/atmos-validation/blob/main/examples/example_ascii_measurement.dat)

## Contributing

We welcome all kinds of contributions, including code, bug reports, issues, feature requests, and documentation. The preferred way of submitting a contribution is to either make an issue on GitHub or by forking the project on GitHub and making a pull requests. In case of bug reports, please provide a detailed explanation for how to reproduce before submitting.
