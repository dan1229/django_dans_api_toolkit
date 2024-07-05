from django.test import TestCase
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ..api_response_handler import ApiResponseHandler


class ApiResponseHandlerTestCase(TestCase):

    def setUp(self) -> None:
        self.api_response_handler = ApiResponseHandler()

    def test_response_success_with_default_message(self) -> None:
        response = self.api_response_handler.response_success()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.data["message"], self.api_response_handler.message_success  # type: ignore[index]
        )

    def test_response_success_with_custom_message(self) -> None:
        custom_message = "Custom success message."
        response = self.api_response_handler.response_success(message=custom_message)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["message"], custom_message)  # type: ignore[index]

    def test_response_success_with_results(self) -> None:
        results = {"key": "value"}
        response = self.api_response_handler.response_success(results=results)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], results)  # type: ignore[index]

    def test_response_error_with_default_message(self) -> None:
        response = self.api_response_handler.response_error()
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], self.api_response_handler.message_error  # type: ignore[index]
        )

    def test_response_error_with_custom_message(self) -> None:
        custom_message = "Custom error message."
        response = self.api_response_handler.response_error(message=custom_message)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], custom_message)  # type: ignore[index]

    def test_response_error_with_validation_error(self) -> None:
        error = ValidationError({"__all__": ["Validation error message."]})
        response = self.api_response_handler.response_error(error=error)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Validation error message.")  # type: ignore[index]

    def test_response_error_with_integrity_error(self) -> None:
        error = IntegrityError("Integrity error message.")
        response = self.api_response_handler.response_error(error=error)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Integrity error message.")  # type: ignore[index]

    def test_response_error_with_error_fields(self) -> None:
        error_fields = {"field": ["Field error message."]}
        response = self.api_response_handler.response_error(error_fields=error_fields)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Field error message.")  # type: ignore[index]

    def test_response_error_logging(self) -> None:
        custom_message = "Log this error."
        error = "Actual error."
        with self.assertLogs("django_dans_api_toolkit", level="ERROR") as cm:
            self.api_response_handler.response_error(
                message=custom_message, error=error
            )
            self.assertIn(f"{custom_message} - {error}", cm.output[0])

    def test_response_success_with_extra_data(self) -> None:
        extra_data = {"extra_key": "extra_value"}
        response = self.api_response_handler.response_success(results=extra_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], extra_data)  # type: ignore[index]

    def test_response_error_with_results(self) -> None:
        results = {"error_key": "error_value"}
        response = self.api_response_handler.response_error(results=results)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["results"], results)  # type: ignore[index]

    def test_response_success_with_mixed_results(self) -> None:
        results = {
            "key": "value",
            "list": [1, 2, 3],
            "dict": {"inner_key": "inner_value"},
        }
        response = self.api_response_handler.response_success(results=results)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], results)  # type: ignore[index]

    def test_response_error_logging_with_custom_message_only(self) -> None:
        custom_message = "Log this error."
        with self.assertLogs("django_dans_api_toolkit", level="ERROR") as cm:
            self.api_response_handler.response_error(message=custom_message)
            self.assertGreater(len(cm.output), 0, "No log output captured.")
            self.assertIn(custom_message, cm.output[0])

    def test_response_error_logging_with_error_only(self) -> None:
        error = "Actual error."
        with self.assertLogs("django_dans_api_toolkit", level="ERROR") as cm:
            self.api_response_handler.response_error(error=error)
            self.assertGreater(len(cm.output), 0, "No log output captured.")
            self.assertIn(error, cm.output[0])
