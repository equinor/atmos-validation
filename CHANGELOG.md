# Changelog

## [2.0.2](https://github.com/equinor/atmos-validation/compare/v2.0.1...v2.0.2) (2025-09-10)


### Bug Fixes

* Fix xarray future warnings ([#66](https://github.com/equinor/atmos-validation/issues/66)) ([2b8ef08](https://github.com/equinor/atmos-validation/commit/2b8ef08248e7f74cf097d179c7dd8d9522bacfe7))


### Optimization

* Fix dataset load performance bottlenecks ([#67](https://github.com/equinor/atmos-validation/issues/67)) ([b899558](https://github.com/equinor/atmos-validation/commit/b899558a13dfe3ffa9138f5ef34836d20f9f8fa2))

## [2.0.1](https://github.com/equinor/atmos-validation/compare/v2.0.0...v2.0.1) (2025-09-09)


### Optimization

* Adjust compatibility settings for open_mfdataset ([#64](https://github.com/equinor/atmos-validation/issues/64)) ([9e5825f](https://github.com/equinor/atmos-validation/commit/9e5825f0d666d135f32d06242514258b8288ba9e))

## [2.0.0](https://github.com/equinor/atmos-validation/compare/v1.11.0...v2.0.0) (2025-09-05)


### ⚠ BREAKING CHANGES

* Upgrade dependencies and supported python versions ([#58](https://github.com/equinor/atmos-validation/issues/58))

### Features

* Upgrade dependencies and supported python versions ([#58](https://github.com/equinor/atmos-validation/issues/58)) ([2de41ee](https://github.com/equinor/atmos-validation/commit/2de41ee8300810d4199f181b9a688e654f09fdd3))


### Optimization

* Increase default batch size ([#63](https://github.com/equinor/atmos-validation/issues/63)) ([512b23b](https://github.com/equinor/atmos-validation/commit/512b23b1f063c323f232c8188e3456703fa903c5))

## [1.11.0](https://github.com/equinor/atmos-validation/compare/v1.10.0...v1.11.0) (2025-09-05)


### Features

* add schema for wpi ([#54](https://github.com/equinor/atmos-validation/issues/54)) ([5219086](https://github.com/equinor/atmos-validation/commit/52190869bff082eb3585662591a7cf5f8c2e2398))


### Bug Fixes

* **CI:** Merge multiple coverage reports ([#53](https://github.com/equinor/atmos-validation/issues/53)) ([b0c6fa3](https://github.com/equinor/atmos-validation/commit/b0c6fa380e93b2d3b56f388a214e4f4a3b8dfbf5))
* Fix 5d spectra validation bug ([#57](https://github.com/equinor/atmos-validation/issues/57)) ([087e09b](https://github.com/equinor/atmos-validation/commit/087e09b25a3e966c7bbc5b6631bae20888a428f7))


### Other

* add GH Action for Trufflehog scans on pull/push to remote branch ([#50](https://github.com/equinor/atmos-validation/issues/50)) ([06b6760](https://github.com/equinor/atmos-validation/commit/06b676004eff983eb8139c407242b06f626afe19))
* adds trufflehog scan pre commit hook  ([#51](https://github.com/equinor/atmos-validation/issues/51)) ([d09fb89](https://github.com/equinor/atmos-validation/commit/d09fb8968fee118af28e63c39924093ca3d566a6))
* remove wpi schema from validation repo ([#55](https://github.com/equinor/atmos-validation/issues/55)) ([0e5e0d4](https://github.com/equinor/atmos-validation/commit/0e5e0d4aa3f06023650db0e5838ec76a27121602))
* UV migration ([#56](https://github.com/equinor/atmos-validation/issues/56)) ([843f799](https://github.com/equinor/atmos-validation/commit/843f799501b10cdbe98bd15f1ea5257a333c9762))

## [1.10.0](https://github.com/equinor/atmos-validation/compare/v1.9.0...v1.10.0) (2025-02-13)


### Features

* add qc_tests schema for GET qc_test config api ([#47](https://github.com/equinor/atmos-validation/issues/47)) ([83fecb2](https://github.com/equinor/atmos-validation/commit/83fecb26941957f590c4405dd6d55783b4d7f6db))


### Bug Fixes

* update ci-test-pr.yml ([#48](https://github.com/equinor/atmos-validation/issues/48)) ([140b58f](https://github.com/equinor/atmos-validation/commit/140b58fe9b3e02871c570699e66b06f1ebdec7f4))

## [1.9.0](https://github.com/equinor/atmos-validation/compare/v1.8.0...v1.9.0) (2025-01-16)


### Features

* add default variable schema for qc test ([#44](https://github.com/equinor/atmos-validation/issues/44)) ([efafe0b](https://github.com/equinor/atmos-validation/commit/efafe0bb93c161a23a3c584754bb96aaada21ddc))


### Bug Fixes

* update parameter config file ([#46](https://github.com/equinor/atmos-validation/issues/46)) ([b6e604b](https://github.com/equinor/atmos-validation/commit/b6e604b09dda8dfdf1fa214212e456fd7248e06e))

## [1.8.0](https://github.com/equinor/atmos-validation/compare/v1.7.0...v1.8.0) (2025-01-14)


### Features

* update qc test schema ([#42](https://github.com/equinor/atmos-validation/issues/42)) ([ec6670c](https://github.com/equinor/atmos-validation/commit/ec6670c3996fc09e23e121504da835e8eac5086a))

## [1.7.0](https://github.com/equinor/atmos-validation/compare/v1.6.2...v1.7.0) (2025-01-08)


### Features

* update parameters config with qc_test ([#40](https://github.com/equinor/atmos-validation/issues/40)) ([c1aac6e](https://github.com/equinor/atmos-validation/commit/c1aac6e9094c14f37a96ec2cd87a767303381c35))

## [1.6.2](https://github.com/equinor/atmos-validation/compare/v1.6.1...v1.6.2) (2024-11-12)


### Other

* Allow final_reports attribute to be "NA" ([#37](https://github.com/equinor/atmos-validation/issues/37)) ([ecf4a99](https://github.com/equinor/atmos-validation/commit/ecf4a995bf4a8216775ba3f8313438194b4d04c3))

## [1.6.1](https://github.com/equinor/atmos-validation/compare/v1.6.0...v1.6.1) (2024-10-22)


### Documentation

* Update ASCII documentation ([#35](https://github.com/equinor/atmos-validation/issues/35)) ([f082780](https://github.com/equinor/atmos-validation/commit/f0827803569ce439b7083c453d5b5830be2a9583))

## [1.6.0](https://github.com/equinor/atmos-validation/compare/v1.5.0...v1.6.0) (2024-10-17)


### Features

* Accept 5d spectral dimensions ([#34](https://github.com/equinor/atmos-validation/issues/34)) ([5787e5c](https://github.com/equinor/atmos-validation/commit/5787e5c480e3f1740a4be0c9f4b02a1e8a224a75))
* creates data_type for single point hindcast ([#32](https://github.com/equinor/atmos-validation/issues/32)) ([9b12c56](https://github.com/equinor/atmos-validation/commit/9b12c56877472d0df9871ade71126e630bfa788e))

## [1.5.0](https://github.com/equinor/atmos-validation/compare/v1.4.2...v1.5.0) (2024-10-07)


### Features

* Update/add final_report validation to validation pipe ([#30](https://github.com/equinor/atmos-validation/issues/30)) ([5b10596](https://github.com/equinor/atmos-validation/commit/5b1059683b2ee01ac4b93650b8e592ee856efc51))


### Bug Fixes

* Set default asset to None ([#29](https://github.com/equinor/atmos-validation/issues/29)) ([08eb62f](https://github.com/equinor/atmos-validation/commit/08eb62fe20ebec817f7b6970cd62eb28ed628e71))

## [1.4.2](https://github.com/equinor/atmos-validation/compare/v1.4.1...v1.4.2) (2024-07-10)


### Other

* Upgrade to Pydantic v2 using TypeAdapters ([#24](https://github.com/equinor/atmos-validation/issues/24)) ([74c3e04](https://github.com/equinor/atmos-validation/commit/74c3e04e16a2e771c2ddd1e6eee8dc398f564255))
* Use ruff formatter ([#25](https://github.com/equinor/atmos-validation/issues/25)) ([c0ef09e](https://github.com/equinor/atmos-validation/commit/c0ef09e5c435fcfe75ab5d83336afe336f6c003a))


### CI/CD

* Add build to "Other" section for release docs ([#27](https://github.com/equinor/atmos-validation/issues/27)) ([865b752](https://github.com/equinor/atmos-validation/commit/865b752fe7782f0e62058f96c4e219b1f52cb28f))
* Fix release-please typo in config ([#28](https://github.com/equinor/atmos-validation/issues/28)) ([fd2b51e](https://github.com/equinor/atmos-validation/commit/fd2b51e7446ff2716f8f296577157186bf9339e7))

## [1.4.1](https://github.com/equinor/atmos-validation/compare/v1.4.0...v1.4.1) (2024-01-09)


### Other

* Python 3.12 support ([#21](https://github.com/equinor/atmos-validation/issues/21)) ([0571ea8](https://github.com/equinor/atmos-validation/commit/0571ea8e086a5af6df649184725de406ffcc26b9))

## [1.4.0](https://github.com/equinor/atmos-validation/compare/v1.3.3...v1.4.0) (2024-01-08)


### Features

* Make batch size a CLI argument ([#19](https://github.com/equinor/atmos-validation/issues/19)) ([270c97c](https://github.com/equinor/atmos-validation/commit/270c97cd49aa8e6e434eabe32a1fa108848b9f26))

## [1.3.3](https://github.com/equinor/atmos-validation/compare/v1.3.2...v1.3.3) (2024-01-04)


### Bug Fixes

* Fix location parsing for south hemisphere locations ([#17](https://github.com/equinor/atmos-validation/issues/17)) ([1d42213](https://github.com/equinor/atmos-validation/commit/1d422131287aa959858d7606aecab0f803107928))

## [1.3.2](https://github.com/equinor/atmos-validation/compare/v1.3.1...v1.3.2) (2023-11-29)


### Bug Fixes

* Make default classification_level "Internal" str ([#14](https://github.com/equinor/atmos-validation/issues/14)) ([fa02ee9](https://github.com/equinor/atmos-validation/commit/fa02ee93360d4ec48d96d92ef8d0cf4d52483252))


### Other

* Add security md from template ([#15](https://github.com/equinor/atmos-validation/issues/15)) ([4042db3](https://github.com/equinor/atmos-validation/commit/4042db392425853a44ee58042667f3fffd2bb265))

## [1.3.1](https://github.com/equinor/atmos-validation/compare/v1.3.0...v1.3.1) (2023-11-21)


### Bug Fixes

* Fix height sorting for data array  ([#12](https://github.com/equinor/atmos-validation/issues/12)) ([4b13e81](https://github.com/equinor/atmos-validation/commit/4b13e818af52b91360f083f115396b02904939dc))

## [1.3.0](https://github.com/equinor/atmos-validation/compare/v1.2.0...v1.3.0) (2023-10-31)


### Features

* Add classification level validation ([#10](https://github.com/equinor/atmos-validation/issues/10)) ([2d1c22f](https://github.com/equinor/atmos-validation/commit/2d1c22f88e71eda48a5e22372326163228f47454))
* Add country as non-optional attribute ([#9](https://github.com/equinor/atmos-validation/issues/9)) ([c26c83c](https://github.com/equinor/atmos-validation/commit/c26c83ccd4afa4d6bb887e8994da6d9fbd5c7e9e))

## [1.2.0](https://github.com/equinor/atmos-validation/compare/v1.1.0...v1.2.0) (2023-10-26)


### Features

* Add metadata tags for country and asset ([#6](https://github.com/equinor/atmos-validation/issues/6)) ([95b70a9](https://github.com/equinor/atmos-validation/commit/95b70a9bef97d70a2e5b920965417de9ddcc2a75))

## [1.1.0](https://github.com/equinor/atmos-validation/compare/v1.0.0...v1.1.0) (2023-10-20)


### Features

* Make memos type allow list of strings ([#3](https://github.com/equinor/atmos-validation/issues/3)) ([71a2413](https://github.com/equinor/atmos-validation/commit/71a24139a9e41fd152cbf1ae491fcc324115b955))


### Documentation

* Use full links in readme ([#4](https://github.com/equinor/atmos-validation/issues/4)) ([f05cdd0](https://github.com/equinor/atmos-validation/commit/f05cdd049c8ea2fd8d8965a746f239f89cae3eb7))

## 1.0.0 (2023-10-10)


### Features

* Add all files from source repo ([#1](https://github.com/equinor/atmos-validation/issues/1)) ([47f64e6](https://github.com/equinor/atmos-validation/commit/47f64e6b3528a8225e5ae662966e1c8b11e53616))


### Other

* release 1.0.0 ([c41a71f](https://github.com/equinor/atmos-validation/commit/c41a71fd442b62a1363f5b284bcbe923d297bcc7))
