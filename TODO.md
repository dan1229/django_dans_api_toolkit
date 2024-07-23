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
### 1.1.0



#### get coverage to 100%
- yup



#### pypi test cd script
- upload to test py on each push



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



### [1.1.0] - 2024-MM-DD
- TODO

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
