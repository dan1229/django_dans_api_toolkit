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



-----
### 1.1.0




#### add detect version workflow to auto release



any other improvements / clean up?


#### add lots of tests?
- at least re-evaluate them
- coverage too i guess


#### taking errors from error fields
- this is working kinda well, some weird cases like:
  - "This field may not be blank."
  - "This field is required."
  - "This field may not be null."
- maybe this just isnt the way? the message should be unchanged
  - these happened in cases where 'message' WAS being passed
    - check MeetingSchedeuleWindowViewSet - create endpoint
-
- helper function to parse validation errors?
    - i.e., if no message, pull it out of particular error types?
    - view get twenty
        - honestly just a lot of boilerplat in the meeting views
            - meeting instance create api
            - meeting schedule window create api
    - can do different error types
        - drf validation
        - django validation
        - integrity
        - base error
        - 'non_field_errors'
            - should this be handled here or the client side response handler?




#### ✅ COMPLETED: error logging improvements
FIXED: ApiResponseHandler now automatically includes stack traces when Exception objects are logged.

Changes made:
- Modified `_handle_logging` method to accept optional `exception` parameter
- When Exception objects are passed to `response_error`, they automatically get logged with `exc_info=True`
- Backward compatible - string errors still work normally without stack traces
- Added comprehensive tests to verify functionality

Now developers can simply do:
```python
try:
    # some operation that might fail
    serializer.is_valid(raise_exception=True)
except (ValidationError, IntegrityError, DRFValidationError) as e:
    return self.response_handler.response_error(
        message="Error logging in user.",
        error=e,  # Exception object automatically gets full stack trace
        error_fields=serializer.errors,
    )
```




### [1.1.0] - 2025-MM-DD
- Improved error logging!
    - logging methods automatically pass exception data to logging handlers
        - No more need for manual `LOGGER.error(f"...", exc_info=True)` boilerplate in viewsets

-------------------------------------------------------

##### Copyright 2025 © Daniel Nazarian.
