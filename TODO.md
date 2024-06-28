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



#### pypi test cd script
- upload to test py on each push



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
- test on get twenty
    - figure out why not working
        - revert to base and work backwards - issue is in this code not get twenty
- remove egg.info folder



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
