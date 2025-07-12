# type: ignore
# This file uses # type: ignore due to DRF's Response.data not being typed as a dict,
# which causes mypy errors under strict settings. All accesses to response.data are safe in these tests.
# Remove this ignore if/when DRF types Response.data as a dict or a suitable stub is used.
from django.test import TestCase
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DRFValidationError
from unittest.mock import MagicMock
from ..api_response_handler import ApiResponseHandler


class ApiResponseHandlerTestCase(TestCase):

    def setUp(self) -> None:
        self.api_response_handler = ApiResponseHandler()

    def test_response_success_with_default_message(self) -> None:
        response = self.api_response_handler.response_success()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.data["message"], self.api_response_handler.message_success
        )

    def test_response_success_with_custom_message(self) -> None:
        custom_message = "Custom success message."
        response = self.api_response_handler.response_success(message=custom_message)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["message"], custom_message)

    def test_response_success_with_results(self) -> None:
        results: dict[str, object] = {"key": "value"}
        response = self.api_response_handler.response_success(results=results)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], results)

    def test_response_error_with_default_message(self) -> None:
        response = self.api_response_handler.response_error()
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], self.api_response_handler.message_error
        )

    def test_response_error_with_custom_message(self) -> None:
        custom_message = "Custom error message."
        response = self.api_response_handler.response_error(message=custom_message)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], custom_message)

    def test_response_error_with_validation_error(self) -> None:
        error = ValidationError({"__all__": ["Validation error message."]})
        response = self.api_response_handler.response_error(error=error)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Validation error message.")

    def test_response_error_with_integrity_error(self) -> None:
        error = IntegrityError("Integrity error message.")
        response = self.api_response_handler.response_error(error=error)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Integrity error message.")

    def test_response_error_with_error_fields(self) -> None:
        error_fields: dict[str, list[str]] = {"field": ["Field error message."]}
        response = self.api_response_handler.response_error(error_fields=error_fields)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Field error message.")

    def test_response_error_logging(self) -> None:
        custom_message = "Log this error."
        error = "Actual error."
        with self.assertLogs("django_dans_api_toolkit", level="ERROR") as cm:
            self.api_response_handler.response_error(
                message=custom_message, error=error
            )
            self.assertIn(f"{custom_message} - {error}", cm.output[0])

    def test_response_success_with_extra_data(self) -> None:
        extra_data: dict[str, object] = {"extra_key": "extra_value"}
        response = self.api_response_handler.response_success(results=extra_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], extra_data)

    def test_response_error_with_results(self) -> None:
        results: dict[str, object] = {"error_key": "error_value"}
        response = self.api_response_handler.response_error(results=results)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["results"], results)

    def test_response_success_with_mixed_results(self) -> None:
        results: dict[str, object] = {
            "key": "value",
            "list": [1, 2, 3],
            "dict": {"inner_key": "inner_value"},
        }
        response = self.api_response_handler.response_success(results=results)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["results"], results)

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

    def test_response_error_logging_with_exception_includes_stack_trace(self) -> None:
        """Test that Exception objects automatically get logged with exc_info=True for stack traces."""
        mock_logger = MagicMock()
        handler = ApiResponseHandler(logger=mock_logger)

        # Create a real exception to test with
        test_exception = ValueError("Test exception message")

        handler.response_error(error=test_exception, message="An error occurred")

        # Verify that logger.error was called with exc_info=True
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args
        self.assertTrue(
            call_args[1].get("exc_info"),
            "exc_info should be True when logging exceptions",
        )
        self.assertIn("An error occurred - Test exception message", call_args[0][0])

    def test_response_error_logging_with_string_error_no_stack_trace(self) -> None:
        """Test that string errors don't get logged with exc_info=True."""
        mock_logger = MagicMock()
        handler = ApiResponseHandler(logger=mock_logger)

        handler.response_error(
            error="String error message", message="An error occurred"
        )

        # Verify that logger.error was called without exc_info=True
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args
        self.assertIsNone(
            call_args[1].get("exc_info"), "exc_info should not be set for string errors"
        )
        self.assertIn("An error occurred - String error message", call_args[0][0])

    def test_response_error_logging_exception_only_with_stack_trace(self) -> None:
        """Test that when only an exception is passed (no custom message), it gets logged with stack trace."""
        mock_logger = MagicMock()
        handler = ApiResponseHandler(logger=mock_logger)

        test_exception = RuntimeError("Runtime error occurred")

        handler.response_error(error=test_exception)

        # Verify that logger.error was called with exc_info=True
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args
        self.assertTrue(
            call_args[1].get("exc_info"),
            "exc_info should be True when logging exceptions",
        )
        self.assertIn("Runtime error occurred", call_args[0][0])

    def test_response_error_logging_disabled_no_calls(self) -> None:
        """Test that when print_log is False, no logging occurs."""
        mock_logger = MagicMock()
        handler = ApiResponseHandler(logger=mock_logger)

        test_exception = ValueError("This should not be logged")

        handler.response_error(error=test_exception, print_log=False)

        # Verify that logger.error was not called
        mock_logger.error.assert_not_called()

    def test_custom_message_priority_over_field_errors(self) -> None:
        """Test that custom message takes priority over error_fields when both are provided."""
        custom_message = "Custom error message for user"
        error_fields: dict[str, list[str]] = {
            "field1": ["This field may not be blank."]
        }

        response = self.api_response_handler.response_error(
            message=custom_message, error_fields=error_fields
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], custom_message)
        self.assertEqual(response.data["error_fields"], error_fields)

    def test_custom_message_priority_over_drf_validation_error(self) -> None:
        """Test that custom message takes priority over DRF-style validation errors."""
        drf_error = DRFValidationError({"field1": ["This field is required."]})
        custom_message = "Custom validation error message"
        error_fields = drf_error.detail if isinstance(drf_error.detail, dict) else None
        response = self.api_response_handler.response_error(
            message=custom_message, error=drf_error, error_fields=error_fields
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], custom_message)
        self.assertEqual(response.data["error_fields"], drf_error.detail)

    def test_error_fields_fallback_when_no_message(self) -> None:
        """Test that error_fields are used for message when no custom message is provided."""
        error_fields: dict[str, list[str]] = {
            "field1": ["This field may not be blank."]
        }

        response = self.api_response_handler.response_error(error_fields=error_fields)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "This field may not be blank.")
        self.assertEqual(response.data["error_fields"], error_fields)

    def test_drf_validation_error_with_non_field_errors(self) -> None:
        """Test DRF ValidationError with non_field_errors is properly parsed."""
        drf_error = DRFValidationError(
            {
                "non_field_errors": ["Unable to log in with provided credentials."],
                "username": ["This field is required."],
            }
        )

        response = self.api_response_handler.response_error(error=drf_error)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], "Unable to log in with provided credentials."
        )

    def test_drf_validation_error_without_non_field_errors(self) -> None:
        """Test DRF ValidationError without non_field_errors uses first field error."""
        drf_error = DRFValidationError(
            {
                "username": ["This field is required."],
                "password": ["This field may not be blank."],
            }
        )

        response = self.api_response_handler.response_error(error=drf_error)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        # Should get the first field error (order may vary, but should be one of them)
        message = response.data["message"]
        self.assertIn(
            message, ["This field is required.", "This field may not be blank."]
        )

    def test_error_fields_with_non_field_errors_priority(self) -> None:
        """Test that non_field_errors in error_fields takes priority over field-specific errors."""
        error_fields: dict[str, list[str]] = {
            "non_field_errors": ["General validation error."],
            "field1": ["This field is required."],
        }

        response = self.api_response_handler.response_error(error_fields=error_fields)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "General validation error.")

    def test_empty_error_fields_uses_default_message(self) -> None:
        """Test that empty error_fields results in default error message."""
        response = self.api_response_handler.response_error(error_fields={})

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], self.api_response_handler.message_error
        )

    def test_generic_exception_parsing(self) -> None:
        """Test that generic exceptions are converted to string messages."""
        custom_error = ValueError("Invalid value provided")

        response = self.api_response_handler.response_error(error=custom_error)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid value provided")

    def test_message_priority_over_all_error_types(self) -> None:
        """Test that custom message always takes priority over any error type."""
        custom_message = "User-friendly error message"
        # Test with Django ValidationError
        django_error = ValidationError({"__all__": ["Django validation failed."]})
        response = self.api_response_handler.response_error(
            message=custom_message, error=django_error
        )
        self.assertEqual(response.data["message"], custom_message)
        # Test with DRF ValidationError
        drf_error = DRFValidationError({"non_field_errors": ["DRF validation failed."]})
        response = self.api_response_handler.response_error(
            message=custom_message, error=drf_error
        )
        self.assertEqual(response.data["message"], custom_message)
        # Test with IntegrityError
        integrity_error = IntegrityError("Database constraint violation")
        response = self.api_response_handler.response_error(
            message=custom_message, error=integrity_error
        )
        self.assertEqual(response.data["message"], custom_message)
        # Test with error_fields
        error_fields: dict[str, list[str]] = {"field1": ["Field validation failed."]}
        response = self.api_response_handler.response_error(
            message=custom_message, error_fields=error_fields
        )
        self.assertEqual(response.data["message"], custom_message)

    def test_complex_drf_validation_error_structure(self) -> None:
        """Test handling of complex DRF ValidationError structures."""
        # Test with nested error structures
        drf_error = DRFValidationError(
            {
                "user": {
                    "email": ["Invalid email format."],
                    "username": ["Username already exists."],
                },
                "password": ["Password too weak."],
            }
        )

        response = self.api_response_handler.response_error(error=drf_error)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        # Should extract some meaningful message from the structure
        message = response.data["message"]
        self.assertIsInstance(message, str)
        self.assertNotEqual(message, self.api_response_handler.message_error)

    def test_extremely_nested_error_structure(self) -> None:
        """Test handling of extremely nested error structures (lists of dicts of lists)."""
        drf_error = DRFValidationError(
            [
                {"outer": [{"inner": ["Deep error message!"]}]},
                {"other": ["Should not be reached."]},
            ]
        )
        response = self.api_response_handler.response_error(error=drf_error)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Deep error message!")

    def test_backwards_compatibility_with_existing_tests(self) -> None:
        """Ensure all existing functionality still works exactly the same."""
        # This test verifies that none of the existing behavior changed

        # Test 1: Default message behavior
        response = self.api_response_handler.response_error()
        self.assertEqual(
            response.data["message"], self.api_response_handler.message_error
        )

        # Test 2: Custom message behavior
        custom_message = "Custom error message."
        response = self.api_response_handler.response_error(message=custom_message)
        self.assertEqual(response.data["message"], custom_message)

        # Test 3: Django ValidationError behavior
        error = ValidationError({"__all__": ["Validation error message."]})
        response = self.api_response_handler.response_error(error=error)
        self.assertEqual(response.data["message"], "Validation error message.")

        # Test 4: IntegrityError behavior
        integrity_error = IntegrityError("Integrity error message.")
        response = self.api_response_handler.response_error(error=integrity_error)
        self.assertEqual(response.data["message"], "Integrity error message.")

        # Test 5: error_fields behavior
        error_fields: dict[str, list[str]] = {"field": ["Field error message."]}
        response = self.api_response_handler.response_error(error_fields=error_fields)
        self.assertEqual(response.data["message"], "Field error message.")

    def test_non_field_errors_are_top_level(self) -> None:
        """Test that non_field_errors are top-level and not inside error_fields."""
        error_fields: dict[str, list[str]] = {
            "non_field_errors": [
                "You have too many pending scouting invites (limit: 5). Please wait for responses before sending more."
            ],
            "recipient": ["This field is required."],
        }
        response = self.api_response_handler.response_error(
            error_fields=error_fields.copy()
        )
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"],
            [
                "You have too many pending scouting invites (limit: 5). Please wait for responses before sending more."
            ],
        )
        self.assertNotIn("non_field_errors", response.data.get("error_fields", {}))

    def test_only_non_field_errors(self) -> None:
        """Test response when only non_field_errors are present."""
        error_fields: dict[str, list[str]] = {"non_field_errors": ["General error."]}
        response = self.api_response_handler.response_error(
            error_fields=error_fields.copy()
        )
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(response.data["non_field_errors"], ["General error."])
        self.assertIsNone(response.data.get("error_fields"))

    def test_only_field_errors(self) -> None:
        """Test response when only field errors are present."""
        error_fields: dict[str, list[str]] = {"field": ["Field error."]}
        response = self.api_response_handler.response_error(
            error_fields=error_fields.copy()
        )
        self.assertNotIn("non_field_errors", response.data)
        self.assertEqual(response.data["error_fields"], {"field": ["Field error."]})

    def test_both_non_field_and_field_errors(self) -> None:
        """Test response when both non_field_errors and field errors are present."""
        error_fields: dict[str, list[str]] = {
            "non_field_errors": ["General error."],
            "field": ["Field error."],
        }
        response = self.api_response_handler.response_error(
            error_fields=error_fields.copy()
        )
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(response.data["non_field_errors"], ["General error."])
        self.assertEqual(response.data["error_fields"], {"field": ["Field error."]})

    def test_both_present_but_non_field_errors_empty(self) -> None:
        """Test response when both present but non_field_errors is empty."""
        error_fields: dict[str, list[str]] = {
            "non_field_errors": [],
            "field": ["Field error."],
        }
        response = self.api_response_handler.response_error(
            error_fields=error_fields.copy()
        )
        # Should not include non_field_errors if empty
        self.assertNotIn("non_field_errors", response.data)
        self.assertEqual(response.data["error_fields"], {"field": ["Field error."]})

    def test_non_field_errors_not_a_list(self) -> None:
        """Test response when non_field_errors is not a list (should still be handled)."""
        # Pass a string instead of a list for non_field_errors
        error_fields = {"non_field_errors": "A string error"}
        response = self.api_response_handler.response_error(error_fields=error_fields)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(response.data["non_field_errors"], ["A string error"])

    def test_error_fields_is_none(self) -> None:
        """Test response when error_fields is None."""
        response = self.api_response_handler.response_error(error_fields=None)
        self.assertNotIn("non_field_errors", response.data)
        self.assertIsNone(response.data.get("error_fields"))

    def test_error_fields_is_empty_dict(self) -> None:
        """Test response when error_fields is an empty dict."""
        response = self.api_response_handler.response_error(error_fields={})
        self.assertNotIn("non_field_errors", response.data)
        self.assertIsNone(response.data.get("error_fields"))

    def test_non_field_errors_is_none(self) -> None:
        """Test response when non_field_errors is present and None."""
        error_fields: dict[str, list[str]] = {"non_field_errors": []}
        response = self.api_response_handler.response_error(
            error_fields=error_fields.copy()
        )
        # Should not include non_field_errors if None
        self.assertNotIn("non_field_errors", response.data)
        self.assertIsNone(response.data.get("error_fields"))

    def test_both_missing(self) -> None:
        """Test response when both error_fields and non_field_errors are missing."""
        response = self.api_response_handler.response_error()
        self.assertNotIn("non_field_errors", response.data)
        self.assertIsNone(response.data.get("error_fields"))
