# Tools

This document is about the tools and helpers offered by this project.


## API Helpers

### `api_response`

The `api_response` class is a simple class that represents an API response. It is meant to be used in conjunction with the `api_response_handler` and `api_response_renderer` classes.

You shouldn't have to use this class directly, but it is available if you need it and to help other classes work.



### `api_response_handler`

The `api_response_handler` class is a class that actually handles and processes the API response. It is meant to be used in conjunction with the `api_response` and `api_response_renderer` classes.

To use it, you'll likely have to do something like this:

```
class ViewSet(viewsets.GenericViewSet):
    ...
    response_handler = ApiResponseHandler()
    ...

    def method(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except (ValidationError, IntegrityError, DRFValidationError) as e:
            return self.response_handler.response_error(
                message="Error logging in user.",
                error=e,  # Exception objects automatically get full stack traces in logs!
                error_fields=serializer.errors,
            )

        response_data = function_that_returns_data()
        return self.response_handler.response_success(
            message="Successfully!", results=response_data
        )
```

There's a lot of flexibility in how you can use this class, but this is a basic example of how you might use it.

The main two available methods are:
- `response_success` - to return a successful response.
- `response_error` - to return an error response.

Each supports a number of parameters, check the files for the most up to date information but some overview:
- `message` - a message to return to the user.
- `results` - the data to return to the user, this will be included in a list.
- `status` - the status code to return, defaults to 200 or 400 depending.
- Error responses:
    - `error` - the error message to return to the user. Can be a string or Exception object.
    - `error_fields` - the fields that caused the error, often with more information.

#### Enhanced Error Logging & Message Extraction

The API response handler provides robust error logging and user-friendly error message extraction. Here's how it works:

| Precedence | Error Type                                      | How Message is Extracted                                  |
|------------|-------------------------------------------------|-----------------------------------------------------------|
| 1          | Django ValidationError with `__all__`            | First message from `__all__` field                        |
| 2          | DRF ValidationError with `non_field_errors`      | First message from `non_field_errors`                     |
| 3          | DRF ValidationError (other fields, nested)       | Recursively finds first string error in any field         |
| 4          | IntegrityError                                   | String representation of the error                        |
| 5          | String errors                                    | Uses the string directly                                  |
| 6          | Other Exception types                            | String representation of the exception                    |
| 7          | `error_fields` dict (recursively)                | Recursively finds first string error, prioritizing `non_field_errors` |

**Why this matters:**
- You always get the most relevant, user-friendly error message, even from complex/nested error structures.
- No more manual `LOGGER.error(..., exc_info=True)` boilerplate—exceptions are logged with stack traces automatically.
- Backwards compatibility: all existing code continues to work unchanged.

**Example: deeply nested error extraction**

Given a DRF ValidationError like:

```python
{
    'user': {
        'profile': {
            'email': ['Invalid email.']
        }
    },
    'password': ['Too short.']
}
```
The handler will always surface the first relevant string error it finds, even if it is several levels deep in a dict or list.

All helpers and handlers now have improved type annotations and docstrings for clarity and best practices.


### `api_response_renderer`

The `api_response_renderer` class is a class that renders the API response. This is basically what Django uses to render the actual JSON and can be used to customize the response format.

To use it, you'll have to do something like this:

```
REST_FRAMEWORK = {
    ...
    "DEFAULT_RENDERER_CLASSES": ("django_dans_api_toolkit.api_response_renderer.ApiResponseRenderer",),
    ...
}
```

This does things like add a `message` field to the response to always be there.



## Serializers

### Base Serializer

The `BaseSerializer` class is a base class that you can use to create your own serializers. It offers some basic functionality that you might want to use in your own serializers.

Some features include:
- `masked` - a list of fields that should be masked in the response. This can be controlled on a per-serializer instance basis.
    - Set this via `masked_fields` in the serializer's `Meta` class.
- `ref_serializer` - whether or not this serializer is a reference serializer. This can significantly help performance optimizations
    - Set this via `ref_fields` in the serializer's `Meta` class.
- `fields` - a list of fields that should be included in the response. This is to help with very specific use cases where you want to limit the fields returned.

