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
### 1.3.0



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




##### set custom logger name
- logs show up in sentry and stuff as 'django_dans_api_toolkit'
    - not a huge deal but definitely would be nice to offer an option
    - a bit misleading




#### add lots of tests?
- at least re-evaluate them
- coverage too i guess


#### pagination detection should use pagination class
- we try to detect whether or not a response is paginated
- we should be able to detect hte pagination class being used and check for that specifically



### [1.3.0] - 2025-MM-DD
- TODO

-------------------------------------------------------

##### Copyright 2025 © Daniel Nazarian.
