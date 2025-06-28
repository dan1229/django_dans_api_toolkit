# CHANGELOG - Django Dan's API Toolkit
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹
#### Contact me at <dnaz@danielnazarian.com>

-------------------------------------------------------

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

-------------------------------------------------------
## [Released]

### [1.0.2] - 2024-07-12
- Added support for Djando 3.1+


### [1.0.1] - 2024-07-05
- Simplify `requirements.txt`
    - Added `requirements-dev.txt` as well
- Added MyPy type checking CI step
- General CI clean up
- Linting improved
- Improved `README.md`


### [1.0.0] - 2024-06-28
- Fix weird error fields handling
    - Will use field errors if no 'better error message'
- TESTS!!!
    - Added tests for all major components including:
        - `BaseSerializer`
        - `ApiResponse`
        - `ApiResponseHandler`
        - `ApiResponseRenderer`
    - CI improvements and test coverage vastly improved
    - Almost 100% test coverage!!!
- Updated package requirements
    - Django 5.0 support
    - Remove support for Python 3.8/9
- Improved API logging


### [0.2.0] - 2024-04-28
- Typing added!
- Removed `.pyi` files


### [0.1.9] - 2024-04-28
- Added `pytyped` file to `setup.cfg`


### [0.1.8] - 2024-04-28
- Added `pytyped` file marker


### [0.1.7] - 2024-04-28
- Version number error in `setup.cfg`


### [0.1.6] - 2024-04-28
- Fix `pyi` file bundling in `setup.cfg`


### [0.1.5] - 2024-04-28
- Version number error in `setup.cfg`


### [0.1.4] - 2024-04-28
- Test type stubs for `BaseSerializer`


### [0.1.3] - 2024-04-28
- Clean up types for `BaseSerializer`


### [0.1.2] - 2024-04-28
- `serializers` - added `__init__.py` to fix local imports


### [0.1.1] - 2024-04-28
- Fixed local imports
- Fixed logging in `api_response_handler`


### [0.1.0] - 2024-04-28
- Added basic API helper components
    - `api_response` - A class to represent API responses
    - `api_response_handler` - A class to handle API responses
    - `api_response_renderer` - A class to render API responses for Django
- `BaseSerializer` - A base class for creating serializers
- Some docs


### [0.0.1] - 2024-04-24
- Initial release on PyPi
- Basic project set up with `README`, `CHANGELOG`, and `LICENSE` files
- Basic CI and testing set up

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)

##### Copyright 2025 © Daniel Nazarian.
