# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/equinor/atmos-validation/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                              |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------------------------------------------- | -------: | -------: | ------: | --------: |
| atmos\_validation/\_\_init\_\_.py                                                 |        0 |        0 |    100% |           |
| atmos\_validation/schemas/\_\_init\_\_.py                                         |       10 |        0 |    100% |           |
| atmos\_validation/schemas/classification\_level.py                                |       26 |        4 |     85% |15, 20, 25, 30 |
| atmos\_validation/schemas/data\_usability\_level.py                               |        4 |        0 |    100% |           |
| atmos\_validation/schemas/data\_usability\_levels.py                              |       11 |        0 |    100% |           |
| atmos\_validation/schemas/dim\_constants.py                                       |       10 |        0 |    100% |           |
| atmos\_validation/schemas/installation\_type.py                                   |        4 |        0 |    100% |           |
| atmos\_validation/schemas/installation\_types.py                                  |       11 |        0 |    100% |           |
| atmos\_validation/schemas/instrument\_type.py                                     |        4 |        0 |    100% |           |
| atmos\_validation/schemas/instrument\_types.py                                    |       11 |        0 |    100% |           |
| atmos\_validation/schemas/metadata.py                                             |       43 |        0 |    100% |           |
| atmos\_validation/schemas/parameter\_config.py                                    |       33 |        0 |    100% |           |
| atmos\_validation/schemas/parameter\_configs.py                                   |       23 |        0 |    100% |           |
| atmos\_validation/schemas/tests/\_\_init\_\_.py                                   |        0 |        0 |    100% |           |
| atmos\_validation/schemas/tests/test\_classification\_level.py                    |        7 |        0 |    100% |           |
| atmos\_validation/schemas/tests/test\_parameter\_configs.py                       |        8 |        0 |    100% |           |
| atmos\_validation/schemas/tests/test\_unique\_configs.py                          |       13 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/\_\_init\_\_.py                                |        1 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/main.py                                        |       69 |       23 |     67% |44-66, 114, 119-120, 156-159 |
| atmos\_validation/validate\_netcdf/tests/\_\_init\_\_.py                          |        0 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_blacklisted\_globals.py            |       12 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_data\_usability\_validation.py     |       25 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_dimvars\_validator.py              |        8 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_final\_reports\_validation.py      |       25 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_height\_depth\_validation.py       |       23 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_height\_longname\_validator.py     |       12 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_installation\_types\_validation.py |       13 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_lat\_lon\_validator.py             |       35 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_main.py                            |       25 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_sig\_digs.py                       |       16 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_spatial\_validators.py             |       21 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_time\_validator.py                 |       21 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_util.py                            |       22 |        1 |     95% |        30 |
| atmos\_validation/validate\_netcdf/tests/test\_varattrs\_validation.py            |       29 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_varinterval\_validator.py          |       35 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/utils.py                                       |       81 |       16 |     80% |72-76, 99, 131-136, 142-147, 151 |
| atmos\_validation/validate\_netcdf/validation\_logger.py                          |       52 |        6 |     88% |     23-28 |
| atmos\_validation/validate\_netcdf/validation\_settings.py                        |       21 |        1 |     95% |        25 |
| atmos\_validation/validate\_netcdf/validators/\_\_init\_\_.py                     |        0 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/dims/\_\_init\_\_.py                |        0 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/dims/dims\_validator.py             |        9 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/dims/dimvars\_validator.py          |       26 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/dims/spatial\_validators.py         |       59 |        4 |     93% |58, 62, 67, 69 |
| atmos\_validation/validate\_netcdf/validators/dims/time\_validator.py             |      100 |       26 |     74% |18, 49, 72-83, 97-105, 129-131, 133, 147, 157, 167 |
| atmos\_validation/validate\_netcdf/validators/file\_attributes.py                 |      110 |       13 |     88% |42-43, 83-88, 111-114, 132-133, 166-167 |
| atmos\_validation/validate\_netcdf/validators/root\_validator.py                  |       17 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/variables/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/variables/sig\_dig\_validator.py    |       33 |        2 |     94% |    27, 53 |
| atmos\_validation/validate\_netcdf/validators/variables/varattrs\_validator.py    |       68 |        3 |     96% |38, 53, 58 |
| atmos\_validation/validate\_netcdf/validators/variables/vardims\_validator.py     |       10 |        1 |     90% |        21 |
| atmos\_validation/validate\_netcdf/validators/variables/variables\_validator.py   |       31 |        1 |     97% |        37 |
| atmos\_validation/validate\_netcdf/validators/variables/varinterval\_validator.py |       85 |       10 |     88% |56, 67, 72, 84, 87, 108, 114-116, 119 |
|                                                                         **TOTAL** | **1312** |  **111** | **92%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/equinor/atmos-validation/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/equinor/atmos-validation/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/equinor/atmos-validation/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/equinor/atmos-validation/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fequinor%2Fatmos-validation%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/equinor/atmos-validation/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.