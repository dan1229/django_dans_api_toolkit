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
### 1.4.0



#### update readme and docs?
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



-----
### 2.0.0 - output-changing fixes, held back from 1.3.0 so nothing downstream breaks

#### response status doesn't match http status
- `response_error` / `response_success` pass the raw `status` param to `Response()`
    - should be `api_response.status` so there's one source of truth
- with `status=None` the body says `"status": 400` but the actual http status is 200
    - drf falls back to 200 when status is None, ApiResponse defaults its own to 400
- breaking: `response_success(status=None)` would flip from http 200 to 400
    - `test_status_none_keeps_existing_behaviour` pins the current quirk; update it with the fix



#### validation error fallback never reaches error_fields
- `_parse_validation_error_message` in `api_response_handler.py`
- docstring promises a 5 step preference order but it's an `elif` chain
    - so step 5 (extract from `error_fields`) is unreachable whenever `error` is truthy
- a django `ValidationError` without `__all__` falls to `elif isinstance(error, Exception)`
    - returns `str(error)`, the raw list repr, instead of a clean message
- either restructure the chain or fix the docstring to describe the type switch it actually is
- breaking: changes the `message` clients see; `test_django_error_without_all_uses_str` pins it



#### BaseSerializer self.kwargs loses the popped keys
- `serializers/base.py` does `self.kwargs = kwargs`, then pops from that same dict
- so `self.kwargs` ends up missing `masked` / `ref_serializer` / `fields` / `mask_as_null`
- wants `dict(kwargs)` if the point was keeping the original call
    - or just delete the attribute, nothing seems to read it
- breaking-ish: a subclass forwarding `**self.kwargs` to a plain ModelSerializer would start
  passing keys it rejects



#### make mask_as_null the default?
- 1.3.0 ships it opt-in; flipping the default changes every masked response shape



#### injected logger ignored for the non-dict response.data warning
- `_format_response` is a staticmethod, so its warning always goes to `DEFAULT_LOGGER`
- routing it through `self.logger` means adding a param to `_format_response`
    - breaking: a subclass overriding `_format_response` with the old signature gets a TypeError
    - `test_non_dict_response_data_ignores_injected_logger` pins the current routing
- maybe make it an instance method, or let callers catch the warning some other way



#### logger fallback in _handle_logging
- `logger = self.logger or DEFAULT_LOGGER` looks dead since `__init__` guarantees a logger
    - kept on purpose: a subclass that sets `self.logger = None` would otherwise crash



### [1.3.0] - 2026-MM-DD
- Added: `mask_as_null` opt-in for `BaseSerializer`. Masked fields keep their key with a `null` value instead of being removed.
    - Set it on the serializer, its `Meta`, or pass `mask_as_null=True`. Default output is unchanged.
    - Nulled fields are read-only, so input for them is ignored.
- Fixed: logging no longer repeats the text when `message` equals the exception's text.
- Test coverage is now 100% (lines and branches); new tests pin existing response behaviour.
- CI: every push to main builds a `.devN` package and publishes it to TestPyPI when `TEST_PYPI_PASSWORD` is set.

-------------------------------------------------------

##### Copyright 2025 © Daniel Nazarian.
