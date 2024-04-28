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
                error=f"{type(e)} - {e}",
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
    - `error` - the error message to return to the user.
    - `error_fields` - the fields that caused the error, often with more information.

It helps manage logging API responses and errors as well.


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

