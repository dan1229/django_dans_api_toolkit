# TODO - Django Dan's API Toolkit
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹

-------------------------------------------------------
## [Unreleased]
----
### Improvements

#### crud library
- TODO


#### validation functions
- TODO


-----
### 1.1.0



#### get coverage to 100%
- yup



-----
### 1.0.0



#### doc improvements
- docs/tools available
- readme should have some overview of the tools available
- badges?
    - pipeline statuses
    - coverage?
- pypi link



#### logging improvements
- file name/lines would be great
    - i.e., which api failed not the api_response_handler itself please
- way to hook into existing loggers or use 'new' one?



#### package requirements improvements and updates
- clean them up a bit
    - require higher python version?
- add support for django 5 and higher
    - add to ci tests
- update docs




#### Django tests!!!
- double check all tests are actually solid
    - any edge cases?
- test on 'client' project somehow?
    - pre release or something?
        - actually just release like 0.99.0 or is there a better way




### [1.0.0] - 2024-06-DD
- Fix weird error fields handling
    - Will use field errors if no 'better error message'
- TESTS!!!
    - Added tests for all major components including:
        - `BaseSerializer`
        - `ApiResponse`
        - `ApiResponseHandler`
        - `ApiResponseRenderer`
    - CI improvements and test coverage vastly improved
#### TODO

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
