# Django Dans API Toolkit

[![Lint](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/lint.yml/badge.svg)](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/lint.yml)
[![Test Python](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/test-python.yml/badge.svg)](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/test-python.yml)
[![codecov](https://codecov.io/gh/dan1229/django_dans_api_toolkit/branch/main/graph/badge.svg?token=TL09HDQWBJ)](https://codecov.io/gh/dan1229/django_dans_api_toolkit)

## Description

**Django Dans API Toolkit** is a Django app to help make building APIs great.

It provides a collection of tools for common API tasks, intended to complement Django Rest Framework (DRF) rather than replace it.

[Available on PyPi](https://pypi.org/project/django-dans-api-toolkit/)

## Features

The toolkit includes:
- **API Response Handler** (`api_response_handler.py`): Standardizes API response formats.
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

def my_view(request):
    handler = ApiResponseHandler()
    data = {"key": "value"}
    return handler.response_success(results=data)
```


#### API Response Renderer


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

##### Copyright 2024 © Daniel Nazarian.

