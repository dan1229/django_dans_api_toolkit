from django.test import TestCase
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ..api_response_handler import ApiResponseHandler


class ApiResponseHandlerTestCase(TestCase):

    def setUp(self):
        self.api_response_handler = ApiResponseHandler()

    def test_response_success_with_default_message(self):
        response = self.api_response_handler.response_success()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.data["message"], self.api_response_handler.message_success
        )

    def test_response_success_with_custom_message(self):
        custom_message = "Custom success message."
        response = self.api_response_handler.response_success(message=custom_message)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["message"], custom_message)

    def test_response_success_with_results(self):
        results = {"key": "value"}
        response = self.api_response_handler.response_success(results=results)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], results)

    def test_response_error_with_default_message(self):
        response = self.api_response_handler.response_error()
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], self.api_response_handler.message_error
        )

    def test_response_error_with_custom_message(self):
        custom_message = "Custom error message."
        response = self.api_response_handler.response_error(message=custom_message)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], custom_message)

    def test_response_error_with_validation_error(self):
        error = ValidationError({"__all__": ["Validation error message."]})
        response = self.api_response_handler.response_error(error=error)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Validation error message.")

    def test_response_error_with_integrity_error(self):
        error = IntegrityError("Integrity error message.")
        response = self.api_response_handler.response_error(error=error)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Integrity error message.")

    def test_response_error_with_error_fields(self):
        error_fields = {"field": ["Field error message."]}
        response = self.api_response_handler.response_error(error_fields=error_fields)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Field error message.")

    def test_response_error_logging(self):
        custom_message = "Log this error."
        error = "Actual error."
        with self.assertLogs("django_dans_api_toolkit", level="ERROR") as cm:
            self.api_response_handler.response_error(
                message=custom_message, error=error
            )
            self.assertIn(f"{custom_message} - {error}", cm.output[0])

    def test_response_error_logging_with_custom_message_only(self):
        custom_message = "Log this error."
        with self.assertLogs("django_dans_api_toolkit", level="ERROR") as cm:
            self.api_response_handler.response_error(message=custom_message)
            self.assertGreater(len(cm.output), 0, "No log output captured.")
            self.assertIn(custom_message, cm.output[0])

    def test_response_error_logging_with_error_only(self):
        error = "Actual error."
        with self.assertLogs("django_dans_api_toolkit", level="ERROR") as cm:
            self.api_response_handler.response_error(error=error)
            self.assertGreater(len(cm.output), 0, "No log output captured.")
            self.assertIn(error, cm.output[0])
