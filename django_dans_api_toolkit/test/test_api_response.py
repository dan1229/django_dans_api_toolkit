from django.test import TestCase
from ..api_response import ApiResponse
from typing import Any


class ApiResponseTestCase(TestCase):

    def test_initialization_with_defaults(self) -> None:
        response = ApiResponse()
        self.assertEqual(response.status, 400)
        self.assertIsNone(response.message)
        self.assertIsNone(response.results)
        self.assertIsNone(response.error_fields)  # revert to None, matches __init__
        self.assertEqual(response.extras, {})

    def test_initialization_with_values(self) -> None:
        status = 200
        message = "Success"
        results: dict[str, Any] = {"key": "value"}
        error_fields = {"field": ["error"]}
        extras = {"extra_key": "extra_value"}

        response = ApiResponse(
            status=status,
            message=message,
            results=results,
            error_fields=error_fields,
            extras=extras,
        )

        self.assertEqual(response.status, status)
        self.assertEqual(response.message, message)
        self.assertEqual(response.results, results)
        self.assertEqual(response.error_fields, error_fields)
        self.assertEqual(response.extras, extras)

    def test_dict_method_with_defaults(self) -> None:
        response = ApiResponse()
        response_dict = response.dict()

        expected_dict: dict[str, Any] = {
            "status": 400,
            "message": None,
            "results": None,
            "error_fields": {},
            "non_field_errors": [],
        }

        self.assertEqual(response_dict, expected_dict)

    def test_dict_method_with_values(self) -> None:
        status = 200
        message = "Success"
        results: dict[str, Any] = {"key": "value"}
        error_fields = {"field": ["error"]}
        extras = {"extra_key": "extra_value"}

        response = ApiResponse(
            status=status,
            message=message,
            results=results,
            error_fields=error_fields,
            extras=extras,
        )
        response_dict = response.dict()

        expected_dict: dict[str, Any] = {
            "status": status,
            "message": message,
            "results": results,
            "error_fields": error_fields,
            "non_field_errors": [],  # add this line
            "extras": {"extra_key": "extra_value"},
        }

        self.assertEqual(response_dict, expected_dict)

    def test_dict_method_with_additional_extras(self) -> None:
        response = ApiResponse(extra1="value1", extra2="value2")
        response_dict = response.dict()

        expected_dict: dict[str, Any] = {
            "status": 400,
            "message": None,
            "results": None,
            "error_fields": {},
            "non_field_errors": [],
            "extras": {"extra1": "value1", "extra2": "value2"},
        }

        self.assertEqual(response_dict, expected_dict)

    def test_dict_method_with_dict_extras(self) -> None:
        response = ApiResponse(extras={"extra1": "value1", "extra2": "value2"})
        response_dict = response.dict()

        expected_dict: dict[str, Any] = {
            "status": 400,
            "message": None,
            "results": None,
            "error_fields": {},
            "non_field_errors": [],
            "extras": {"extra1": "value1", "extra2": "value2"},
        }

        self.assertEqual(response_dict, expected_dict)
