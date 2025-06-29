# TODO - Django Dan's API Toolkit
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹

-------------------------------------------------------
## [Unreleased]
----
### Improvements

#### crud library
- make a library for crud operations for django apis
- something to allow each endpoint to just define the model and the viewset


#### validation functions
- validation functions for apis
- things like:
    - validate email
    - validate phone number
    - validate passwords


-----
### 1.2.0



#### get coverage to 100%
- yup



#### pypi test cd script
- upload to test py on each push



#### masked fields shouldn't be removed
- i.e., don't remove the key just put "MASKED" or something?
    - maybe make this an option?
    - by default show the key with no value
    


#### update readme and docs?
- more badges?
- other docs could use clean up
- add docs
    - models?
    - serializers?
    - api response?
    - something to describe the different tools available overall?




##### set custom logger name?
- logs show up in sentry and stuff as 'django_dans_api_toolkit'
    - not a huge deal but definitely would be nice to offer an option
    - a bit misleading


-----
### 1.1.0







any other improvements / clean up?



confirm that we're putting secrets - like pypi password - safetly for a public repo



#### add lots of tests?
- at least re-evaluate them
- coverage too i guess






### [1.1.0] - 2025-MM-DD
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

-------------------------------------------------------

##### Copyright 2025 © Daniel Nazarian.
