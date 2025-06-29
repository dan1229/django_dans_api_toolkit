# Django Dans API Toolkit

[![Lint](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/python-lint.yml/badge.svg)](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/python-lint.yml)
[![Test](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/python-test.yml/badge.svg)](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/python-test.yml)
[![Types](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/python-types.yml/badge.svg)](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/python-types.yml)
[![codecov](https://codecov.io/gh/dan1229/django_dans_api_toolkit/branch/main/graph/badge.svg?token=TL09HDQWBJ)](https://codecov.io/gh/dan1229/django_dans_api_toolkit)

[![Python Versions](https://img.shields.io/pypi/pyversions/django-dans-api-toolkit.svg?color=3776AB&logo=python&logoColor=white)](https://www.python.org/)
[![Django Versions](https://img.shields.io/pypi/djversions/django-dans-api-toolkit?color=0C4B33&logo=django&logoColor=white&label=django)](https://www.djangoproject.com/)
[![PyPI Version](https://img.shields.io/pypi/v/django-dans-api-toolkit.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/django-dans-api-toolkit/)
[![Downloads](https://static.pepy.tech/badge/django-dans-api-toolkit/month)](https://pepy.tech/project/django-dans-api-toolkit)
[![License](https://img.shields.io/pypi/l/django-dans-api-toolkit.svg?color=blue)](https://github.com/dan1229/django-dans-api-toolkit/blob/main/LICENSE.txt)
[![Codacy grade](https://img.shields.io/codacy/grade/21cb657283c04e70b56fb935277a1ad1?logo=codacy)](https://www.codacy.com/app/dan1229/django-dans-api-toolkit)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=black)](https://github.com/psf/black)

## Description

**Django Dans API Toolkit** is a Django app to help make building APIs great.

It provides a collection of tools for common API tasks, intended to complement Django Rest Framework (DRF) rather than replace it.

[Available on PyPi](https://pypi.org/project/django-dans-api-toolkit/)

## Features

The toolkit includes:
- **API Response Handler** (`api_response_handler.py`): Standardizes API response formats with enhanced error logging that automatically captures stack traces for Exception objects. Now with robust error message extraction that supports arbitrarily nested error structures (for example, DRF ValidationError details like `{ 'user': { 'profile': { 'email': ['Invalid email.'] } }, 'password': ['Too short.'] }`). The handler will always surface the first relevant string error it finds, even if it is several levels deep in a dict or list, ensuring user-friendly error messages regardless of how complex the error structure is. Type annotations and docstrings have also been improved for clarity and best practices.
- **API Response Renderer** (`api_response_renderer.py`): Ensures consistent response rendering across your APIs.
- **Base Serializer** (`serializers/base.py`): Simplifies serializer creation with masking and reference functionality.

## Quick Start

### Installation

1. **Install the package via pip:**

    ```bash
    pip install django-dans-api-toolkit
    ```

2. **Add `django_dans_api_toolkit` to your `INSTALLED_APPS` setting:**

    ```python
    INSTALLED_APPS = [
        ...
        'django_dans_api_toolkit',
    ]
    ```

3. **Run migrations to update your database schema:**

    ```bash
    python manage.py migrate
    ```

4. **Use the provided tools in your views and serializers.**

### Example Usage

#### API Response Handler

```python
from django_dans_api_toolkit.api_response_handler import ApiResponseHandler
from django.core.exceptions import ValidationError

def my_view(request):
    handler = ApiResponseHandler()
    
    try:
        # Your API logic here
        serializer.is_valid(raise_exception=True)
        data = {"key": "value"}
        return handler.response_success(results=data)
    except ValidationError as e:
        # Exception objects automatically get full stack traces in logs! 
        # Error message extraction also supports arbitrarily nested error structures.
        return handler.response_error(
            message="Validation failed",
            error=e, 
            error_fields=serializer.errors
        )
```


#### Base Serializer

```python
from django_dans_api_toolkit.serializers.base import BaseSerializer
from myapp.models import MyModel

class MyModelSerializer(BaseSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
        ref_fields = ['field1', 'field2']
        masked_fields = ['field3']
```


#### API Response Renderer

Ensure `DEFAULT_AUTHENTICATION_CLASSES` and `DEFAULT_PAGINATION_CLASS` are set in your settings.py for proper API functionality. Set the renderer itself as well.

Example configuration:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}
```


### Requirements
- Python 3.10 - 3.11
- Django 3.1 or higher
- Django Rest Framework
  - **NOTE:** not only must you have this installed, you must have set `DEFAULT_AUTHENTICATION_CLASSES` and `DEFAULT_PAGINATION_CLASS` in your `settings.py` to work with the APIs properly. An example config would be:



-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)

##### Copyright 2025 © Daniel Nazarian.
