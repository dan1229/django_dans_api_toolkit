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
    


-----
### 1.1.0



#### paths arent resolving



#### update readme and docs?
- more badges?
- other docs could use clean up
- add docs
    - models?
    - serializers?
    - api response?
    - something to describe the different tools available overall?



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




#### error logging doesnt work
needed to add manual stack trace / logging to this
- UserLoginViewSet

try:
    # not masked because on login we want all the info
    serializer = self.serializer_class(data=request.data, masked=False)
    serializer.is_valid(raise_exception=True)
except (ValidationError, IntegrityError, DRFValidationError) as e:
    LOGGER.error(f"Error logging in user: {e}", exc_info=True)
    return self.response_handler.response_error(
        message="Error logging in user.",
        error=f"{type(e)} - {e}",
        error_fields=serializer.errors,
    )




### [1.1.0] - 2024-MM-DD
- TODO

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
