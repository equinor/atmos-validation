# atmos-validation

[![SCM Compliance](https://scm-compliance-api.radix.equinor.com/repos/equinor/8f11dd2d-6bdc-4544-9aba-de642f86ec3e/badge)](https://developer.equinor.com/governance/scm-policy/)
[![Build](https://github.com/equinor/atmos-validation/actions/workflows/ci-test-pr.yml/badge.svg)](https://github.com/equinor/atmos-validation/actions/workflows/ci-test-pr.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/licenses/mit)
[![Coverage badge](https://github.com/equinor/atmos-validation/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/equinor/atmos-validation/tree/python-coverage-comment-action-data)

A library containing validation checks to be run on hindcast or measurement data to ensure API compliance and standardization.

Atmos is a project to streamline discoverability and data access for weather data sources through APIs. The first step to building a lean and efficient API is converting data to the standard format.

## Data Validation

In order to ingest measurement or hindcast data into the Atmos Data Store, each source file needs to pass validation. Validation ensures that the file is compliant with the data conventions specified in [Conventions](https://github.com/equinor/atmos-validation/blob/main/docs/conventions.md). The standard file formats for source files are NetCDF files for hindcasts and ASCII or NetCDF for measurements.

Measurements by definition contain data for a single geographical location, whereas hindcasts are bigger models containing time series for a multitude of locations in (possibly rotated) grids. A measurement file is therefore expected to contain all of its data in a single file. A hindcast is comprised of a set of NetCDF files - all with the same coordinates, attributes, and variables, - where a single file contains data for a unique time period. Depending on the size of the files, the time separation should be either monthly or yearly. A rule-of-thumb is that if the file size grows more than 4 GB, it should be split into smaller files. See [docs](https://github.com/equinor/atmos-validation/blob/main/docs/conventions.md#11-time) or [example](https://github.com/equinor/atmos-validation/tree/main/examples/hindcast_example) for how to name hindcast files.

To run validation on NetCDF and ASCII source files, we have built the atmos_validation CLI/library. The documentation below describes these checks, the standard format, and how to run validation using the CLI tool.

## Documentation

- [Conventions](https://github.com/equinor/atmos-validation/blob/main/docs/conventions.md)
- [ASCII Format](https://github.com/equinor/atmos-validation/blob/main/docs/ascii_format.md)
- [Running CLI](https://github.com/equinor/atmos-validation/blob/main/docs/run.md)

## Examples

- [Hindcast netcdfs format example](https://github.com/equinor/atmos-validation/tree/main/examples/hindcast_example)
- [Measurement netcdf format example](https://github.com/equinor/atmos-validation/blob/main/examples/example_netcdf_measurement.nc)
- [Measurement ascii format example](https://github.com/equinor/atmos-validation/blob/main/examples/example_ascii_measurement.dat)

## Contributing

We welcome different types of contributions, including code, bug reports, issues, feature requests, and documentation. The preferred method of submitting a contribution is either to make an issue on GitHub or to fork the project on GitHub and make a pull request. In the case of bug reports, please provide a detailed explanation describing how to reproduce before submitting.

Before making your initial commit, please run:

```pre-commit install```

This sets up a Git hook to automatically run checks (like trufflehog secret scanning) every time you commit. You only need to run this command once — after that, the checks will run automatically.
