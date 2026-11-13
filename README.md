# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/equinor/atmos-validation/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                              |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------------------------------------------- | -------: | -------: | ------: | --------: |
| atmos\_validation/\_\_init\_\_.py                                                 |        0 |        0 |    100% |           |
| atmos\_validation/convert\_ascii/\_\_init\_\_.py                                  |        1 |        0 |    100% |           |
| atmos\_validation/convert\_ascii/attrs\_to\_meta.py                               |       30 |        3 |     90% |  9-10, 53 |
| atmos\_validation/convert\_ascii/df\_to\_nc.py                                    |       82 |       67 |     18% |21-24, 28-55, 59-89, 93-114 |
| atmos\_validation/convert\_ascii/main.py                                          |        9 |        5 |     44% |     16-21 |
| atmos\_validation/convert\_ascii/parsers.py                                       |       73 |       57 |     22% |40-60, 67-113, 117-133, 143-149, 160-182 |
| atmos\_validation/convert\_ascii/tests/\_\_init\_\_.py                            |        0 |        0 |    100% |           |
| atmos\_validation/convert\_ascii/tests/test\_attrs\_to\_meta.py                   |       25 |        0 |    100% |           |
| atmos\_validation/convert\_ascii/tests/test\_parsers.py                           |        9 |        0 |    100% |           |
| atmos\_validation/convert\_ascii/utils.py                                         |       70 |       38 |     46% |28-39, 52-65, 70-71, 76-79, 83-87, 121-127, 131-132, 143-151 |
| atmos\_validation/schemas/\_\_init\_\_.py                                         |       12 |        0 |    100% |           |
| atmos\_validation/schemas/classification\_level.py                                |       26 |        4 |     85% |15, 20, 25, 30 |
| atmos\_validation/schemas/contractor.py                                           |       37 |        5 |     86% | 19, 29-32 |
| atmos\_validation/schemas/data\_usability\_level.py                               |        9 |        1 |     89% |        14 |
| atmos\_validation/schemas/data\_usability\_levels.py                              |       10 |        0 |    100% |           |
| atmos\_validation/schemas/dim\_constants.py                                       |       13 |        0 |    100% |           |
| atmos\_validation/schemas/installation\_type.py                                   |        9 |        1 |     89% |        14 |
| atmos\_validation/schemas/installation\_types.py                                  |       10 |        0 |    100% |           |
| atmos\_validation/schemas/instrument\_type.py                                     |        9 |        1 |     89% |        14 |
| atmos\_validation/schemas/instrument\_types.py                                    |       10 |        0 |    100% |           |
| atmos\_validation/schemas/metadata.py                                             |       18 |        0 |    100% |           |
| atmos\_validation/schemas/parameter\_config.py                                    |       37 |        1 |     97% |        52 |
| atmos\_validation/schemas/parameter\_configs.py                                   |       22 |        0 |    100% |           |
| atmos\_validation/schemas/qc\_tests.py                                            |       10 |        2 |     80% |     17-18 |
| atmos\_validation/schemas/tests/\_\_init\_\_.py                                   |        0 |        0 |    100% |           |
| atmos\_validation/schemas/tests/test\_classification\_level.py                    |        7 |        0 |    100% |           |
| atmos\_validation/schemas/tests/test\_parameter\_configs.py                       |        8 |        0 |    100% |           |
| atmos\_validation/schemas/tests/test\_unique\_configs.py                          |       13 |        0 |    100% |           |
| atmos\_validation/validate\_ascii/\_\_init\_\_.py                                 |        1 |        0 |    100% |           |
| atmos\_validation/validate\_ascii/date\_helper.py                                 |       26 |       19 |     27% |14-22, 25-38 |
| atmos\_validation/validate\_ascii/header\_date.py                                 |       72 |       57 |     21% |9, 12-17, 20, 23, 26, 29-35, 40-71, 74-80, 83, 86, 89-101 |
| atmos\_validation/validate\_ascii/header\_metadata.py                             |       44 |       29 |     34% |34-35, 38-43, 46-51, 54, 58-66, 69-72, 77-79 |
| atmos\_validation/validate\_ascii/header\_names.py                                |       20 |        0 |    100% |           |
| atmos\_validation/validate\_ascii/header\_parameter\_info.py                      |       44 |       24 |     45% |21, 25-28, 31-34, 40-44, 50-59 |
| atmos\_validation/validate\_ascii/header\_parameter\_info\_list.py                |      102 |       86 |     16% |20-54, 59-66, 69, 72, 77, 80, 83-107, 110-123, 126-131, 135-201 |
| atmos\_validation/validate\_ascii/header\_parser.py                               |       58 |       40 |     31% |30-52, 56-62, 65-70, 73, 76-137 |
| atmos\_validation/validate\_ascii/header\_position.py                             |       50 |        5 |     90% |42-43, 57-58, 80 |
| atmos\_validation/validate\_ascii/main.py                                         |       78 |       61 |     22% |21-73, 79-80, 84-96, 100-116 |
| atmos\_validation/validate\_ascii/result\_file.py                                 |        3 |        0 |    100% |           |
| atmos\_validation/validate\_ascii/row\_parser.py                                  |      147 |      122 |     17% |23-26, 29-59, 70-96, 101-126, 131-135, 140-194, 199-219, 228-234, 239-243, 252-261, 266-273, 276-277, 284-291, 303-327 |
| atmos\_validation/validate\_ascii/tests/\_\_init\_\_.py                           |        0 |        0 |    100% |           |
| atmos\_validation/validate\_ascii/tests/test\_contractor\_validation.py           |       46 |        0 |    100% |           |
| atmos\_validation/validate\_ascii/tests/test\_header\_position.py                 |       26 |        0 |    100% |           |
| atmos\_validation/validate\_ascii/utils.py                                        |       30 |       17 |     43% |13, 17-34, 39-44, 49-54 |
| atmos\_validation/validate\_ascii/validate\_result.py                             |       13 |        4 |     69% |12-13, 16, 19 |
| atmos\_validation/validate\_netcdf/\_\_init\_\_.py                                |        1 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/external\_reference\_guard.py                  |       34 |        3 |     91% |44, 49, 53 |
| atmos\_validation/validate\_netcdf/main.py                                        |       74 |       26 |     65% |52-80, 108, 125, 177-180 |
| atmos\_validation/validate\_netcdf/tests/\_\_init\_\_.py                          |        0 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_averaging\_period\_validation.py   |       30 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_blacklisted\_globals.py            |       12 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_contractor\_validation.py          |      111 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_coordinate\_values\_validator.py   |       33 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_data\_usability\_validation.py     |       25 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_dimvars\_validator.py              |        8 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_external\_reference\_guard.py      |       39 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_file\_attributes.py                |       14 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_final\_reports\_validation.py      |       41 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_height\_depth\_validation.py       |       23 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_height\_longname\_validator.py     |       12 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_installation\_types\_validation.py |       13 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_instrument\_counts\_validation.py  |       17 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_lat\_lon\_validator.py             |       35 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_location\_validation.py            |       25 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_main.py                            |       41 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_metadata\_schema\_validation.py    |       63 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_sig\_digs.py                       |       16 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_spatial\_validators.py             |       12 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_time\_validator.py                 |       21 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_total\_water\_depth\_validation.py |       27 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_util.py                            |       22 |        1 |     95% |        30 |
| atmos\_validation/validate\_netcdf/tests/test\_varattrs\_validation.py            |       29 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/tests/test\_varinterval\_validator.py          |       41 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/utils.py                                       |       87 |       12 |     86% |32, 121, 153-158, 164-169, 173 |
| atmos\_validation/validate\_netcdf/validation\_logger.py                          |       52 |        6 |     88% |     23-28 |
| atmos\_validation/validate\_netcdf/validation\_settings.py                        |       55 |       10 |     82% |43-45, 47-49, 62-64, 66 |
| atmos\_validation/validate\_netcdf/validators/\_\_init\_\_.py                     |        0 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/dims/\_\_init\_\_.py                |        0 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/dims/dims\_validator.py             |        9 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/dims/dimvars\_validator.py          |       26 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/dims/spatial\_validators.py         |       83 |        4 |     95% |53, 57, 62, 64 |
| atmos\_validation/validate\_netcdf/validators/dims/time\_validator.py             |      100 |       26 |     74% |18, 49, 72-83, 97-105, 129-131, 133, 147, 157, 167 |
| atmos\_validation/validate\_netcdf/validators/file\_attributes.py                 |      236 |       27 |     89% |128, 132, 198-200, 229-232, 250-251, 273-274, 299-302, 332-333, 352-355, 378-379, 404-405 |
| atmos\_validation/validate\_netcdf/validators/root\_validator.py                  |       17 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/variables/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| atmos\_validation/validate\_netcdf/validators/variables/sig\_dig\_validator.py    |       39 |        5 |     87% |     67-72 |
| atmos\_validation/validate\_netcdf/validators/variables/varattrs\_validator.py    |       68 |        3 |     96% |38, 53, 58 |
| atmos\_validation/validate\_netcdf/validators/variables/vardims\_validator.py     |       10 |        1 |     90% |        21 |
| atmos\_validation/validate\_netcdf/validators/variables/variables\_validator.py   |       29 |        1 |     97% |        36 |
| atmos\_validation/validate\_netcdf/validators/variables/varinterval\_validator.py |      108 |       18 |     83% |32-33, 67-72, 87, 98, 102, 115, 119, 141, 149-151, 153 |
| **TOTAL**                                                                         | **3057** |  **792** | **74%** |           |


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