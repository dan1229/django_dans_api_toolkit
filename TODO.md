# TODO - Django Dan's API Toolkit
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹

-------------------------------------------------------
## [Unreleased]
-----
### 1.0.0


-----
#### Django tests!!!


##### base serializer
- TODO


##### api response
- TODO


##### api response handler
- TODO


##### api response renderer
- TODO


-----

#### crud library
- TODO


#### validation functions
- TODO


#### doc improvements
- docs/tools
- readme should have some overview of the tools available



#### logging improvements
- file name/lines would be great



#### typing - add stubs
- anything else to do?
- https://docs.python.org/3/library/typing.html
- add to:
    - base serializer
    - api_response
    - api_response_handler
    - api_response_renderer



#### package requiements
- clean them up a bit
    - require higher python version?
- update docs



#### error fields
- some weird cases like this:
```
--
[14/May/2024]: ERROR (api_response_handler.py:83)
Error updating user profile. - {'profile_image': [ErrorDetail(string='Upload a valid image. The file you uploaded was either not an image or a corrupted image.', code='invalid_image')]}
--
```
- weird logging from `api_response_handler.handle_error`
- this will have a `message` set to the default though
    - should `message` be set manually if not set?


### [1.0.0] - 2024-MM-DD
#### TODO

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
