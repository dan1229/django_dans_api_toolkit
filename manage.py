#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

# NOTE
# This is NOT really supposed to be used like this :/
# This is primarily used for generating migrations
# and other 'simpler' Django commands


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "django_dans_api_toolkit.test.settings"
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
