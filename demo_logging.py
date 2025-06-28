#!/usr/bin/env python

import os
import logging
import django
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_dans_api_toolkit.test.settings")
django.setup()

# Import after Django setup (required for Django apps)
from django_dans_api_toolkit.api_response_handler import (
    ApiResponseHandler,
)  # noqa: E402

# Configure logging to see the output
logging.basicConfig(
    level=logging.ERROR, format="%(name)s - %(levelname)s - %(message)s"
)


def demo_logging():
    handler = ApiResponseHandler()

    print("=" * 80)
    print("DEMO: Error Logging Improvements")
    print("=" * 80)

    print("\n1. STRING ERROR (no stack trace):")
    print("-" * 40)
    handler.response_error(
        message="User authentication failed", error="Invalid credentials provided"
    )

    print("\n2. EXCEPTION OBJECT (automatic stack trace):")
    print("-" * 40)
    try:
        # Create a realistic exception scenario
        raise ValueError("Database connection timeout after 30 seconds")
    except ValueError as e:
        handler.response_error(
            message="Database operation failed",
            error=e,  # This will automatically get stack trace!
        )

    print("\n3. VALIDATION ERROR (automatic stack trace):")
    print("-" * 40)
    try:
        raise ValidationError("Email field is required")
    except ValidationError as e:
        handler.response_error(message="Form validation failed", error=e)

    print("\n4. INTEGRITY ERROR (automatic stack trace):")
    print("-" * 40)
    try:
        raise IntegrityError("UNIQUE constraint failed: user.email")
    except IntegrityError as e:
        handler.response_error(message="User registration failed", error=e)

    print("\n5. BACKWARD COMPATIBILITY - Old way still works:")
    print("-" * 40)
    handler.response_error(
        message="Legacy error handling", error="This is a string error like before"
    )

    print("\n" + "=" * 80)
    print("Notice how exceptions automatically get stack traces!")
    print("=" * 80)


if __name__ == "__main__":
    demo_logging()
