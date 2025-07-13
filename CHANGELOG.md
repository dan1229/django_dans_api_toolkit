# CHANGELOG - Django Dan's API Toolkit
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹
#### Contact me at <dnaz@danielnazarian.com>

-------------------------------------------------------

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

-------------------------------------------------------
## [Released]

### [1.2.0] - 2025-07-13
- BREAKING: API response structure has been updated for consistency and DRF compatibility.
    - `error_fields` is now always a dict (empty if no errors), never `None`.
    - `non_field_errors` is now always a list (empty if no errors), never `None` or missing.
    - Paginated responses always include all DRF pagination keys (`count`, `next`, `previous`, `results`) at the top level, defaulting to `None` if missing.
- All tests and downstream compatibility have been updated to reflect these changes.


### [1.1.2] - 2025-07-12
- Fixed: Paginated API responses now preserve DRF's top-level pagination keys (`count`, `next`, `previous`, `results`).
    - Ensures full compatibility with DRF clients, tests, and third-party tools expecting standard pagination structure.
    - Custom fields (`status`, `message`, etc.) are still included at the top level.
- This update resolves issues where `count` and other pagination keys were missing from responses, breaking some client integrations and tests.


### [1.1.1] - 2025-07-11
- `non_field_errors` are now always returned as a top-level key in API responses, matching DRF conventions.
    - They are no longer included inside `error_fields`. This ensures compatibility with DRF clients and old tests, and improves error clarity.

    
### [1.1.0] - 2025-06-28
- Improved error logging!
    - logging methods automatically pass exception data to logging handlers
        - No more need for manual `LOGGER.error(f"...", exc_info=True)` boilerplate in viewsets
- Enhanced error field parsing and message creation!
    - Added robust helper function `_parse_validation_error_message()` to handle different validation error types
    - Improved support for DRF ValidationError with `non_field_errors` priority
    - Better handling of complex nested error structures 
    - Custom messages now always take absolute priority over any error type
- As always - tests, tests, tests
- Added `detect-version` Github workflow for auto releases


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
