# Django Dans API Toolkit

[![Lint](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/lint.yml/badge.svg)](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/lint.yml)
[![Test Python](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/test-python.yml/badge.svg)](https://github.com/dan1229/django_dans_api_toolkit/actions/workflows/test-python.yml)
[![codecov](https://codecov.io/gh/dan1229/django_dans_api_toolkit/branch/main/graph/badge.svg?token=TL09HDQWBJ)](https://codecov.io/gh/dan1229/django_dans_api_toolkit)

## Description

A Django app to help make building APIs great.

This app is meant to be a collection of tools to help with common API tasks, and is not meant to be a full-fledged API solution. It is meant to be used in conjunction with Django Rest Framework, and is not a replacement for it.

## Quick start

1. Install the package via pip:

```bash
pip install django-dans-api-toolkit
```

2. Add `django_dans_api_toolkit` to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
	...
	'django_dans_api_toolkit',
]
```

3. Run `python manage.py migrate` to update your database schema.

4. Use the API endpoints, in code or your Django admin portal.

### Requirements

TODO validate these
- Python 3.10 - 3.11
- Django 3.1 or higher
- Django Rest Framework
  - **NOTE:** not only must you have this installed, you must have set `DEFAULT_AUTHENTICATION_CLASSES` and `DEFAULT_PAGINATION_CLASS` in your `settings.py` to work with the APIs properly. An example config would be:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}
```

## Features

This app is meant to be a collection of tools to help with common API tasks, and is not meant to be a full-fledged API solution. It is meant to be used in conjunction with Django Rest Framework, and is not a replacement for it.

Some of the features include:
- API response handler - `api_response_handler.py`
- API response renderer - `api_response_renderer.py`
- Base serializer - `serializers/base.py`

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)

##### Copyright 2024 © Daniel Nazarian.

