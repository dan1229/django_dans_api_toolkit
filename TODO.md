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



#### logging could be better
- lots of logs look like this:
```
    method()
  File "/Users/daniel/projects/get_twenty/server/api/test/user_account_tests/test_settings_scout_view_set.py", line 77, in test_update_settings_scout_missing_pk
    response = self.view_update(request, pk=invalid_pk)
  File "/Users/daniel/.local/share/virtualenvs/server-VHYBaMAB/lib/python3.10/site-packages/django/views/decorators/csrf.py", line 56, in wrapper_view
    return view_func(*args, **kwargs)
  File "/Users/daniel/.local/share/virtualenvs/server-VHYBaMAB/lib/python3.10/site-packages/rest_framework/viewsets.py", line 125, in view
    return self.dispatch(request, *args, **kwargs)
  File "/Users/daniel/.local/share/virtualenvs/server-VHYBaMAB/lib/python3.10/site-packages/rest_framework/views.py", line 506, in dispatch
    response = handler(request, *args, **kwargs)
  File "/Users/daniel/projects/get_twenty/server/api/views/user_accounts.py", line 439, in update
    settings_scout = self.get_object()
  File "/Users/daniel/projects/get_twenty/server/api/views/user_accounts.py", line 424, in get_object
    return self.response_handler.response_error(
  File "/Users/daniel/.local/share/virtualenvs/server-VHYBaMAB/lib/python3.10/site-packages/django_dans_api_toolkit/api_response_handler.py", line 285, in response_error
    self._handle_logging(
  File "/Users/daniel/.local/share/virtualenvs/server-VHYBaMAB/lib/python3.10/site-packages/django_dans_api_toolkit/api_response_handler.py", line 98, in _handle_logging
    logger.error(msg, exc_info=True, stack_info=True)
..Error updating settings. - {'industries_interested_i
```
- can we avoid the stacktrace from this app?


### [1.3.0] - 2025-MM-DD
- TODO

-------------------------------------------------------

##### Copyright 2025 © Daniel Nazarian.
