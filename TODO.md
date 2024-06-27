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



TODO



-----
### 1.0.0


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


#### doc improvements
- docs/tools available
- readme should have some overview of the tools available
- badges?
    - pipeline statuses
    - coverage?
- pypi link



#### logging improvements
- file name/lines would be great
- get rid of ALL prints and stuff



#### package requirements
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
- Fix weird error fields handling
    - Will use field errors if no 'better error message'
#### TODO

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
