from typing import Any, Dict, List, Optional, Union
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import ValidationError as DRFValidationError
import logging

from .api_response import ApiResponse

DEFAULT_LOGGER = logging.getLogger("django_dans_api_toolkit")

"""
============================================================================================ #
API RESPONSE HANDLER ======================================================================= #
============================================================================================ #
"""


class ApiResponseHandler:
    """
    Generic response handler to help manage API responses

    This is used out of the box to provide standardized response formats,
    as well as a centralized place to edit/mangle said responses.

    Mainly just 'wrap' Responses/data you are already returning, this class
    can help enforce structure or format such that you can have responses
    look however you choose.

    It works very closely with the ApiResponse class.
    """

    def __init__(
        self,
        message_error: str = "Error. Please try again later.",
        message_success: str = "Successfully completed request.",
        logger: Optional[logging.Logger] = None,
    ):
        self.message_error = message_error
        self.message_success = message_success
        self.logger = logger or DEFAULT_LOGGER

    @staticmethod
    def _format_response(
        response: Optional[Response] = None,
        results: Optional[Union[object, Dict[Any, Any], List[Any]]] = None,
        message: Optional[str] = None,
        status: Optional[int] = None,
        error_fields: Optional[Dict[Any, Any]] = None,
        non_field_errors: Optional[List[Any]] = None,
    ) -> Response:
        """Internal function to format responses.

        Args:
            response (Response): Existing DRF response object to use for response.
            results (list): List of results to include in response.
            message (str): Message to include in response.
            status (int): Status to use in response.
            error_fields (dict, optional): Dictionary of field errors to include - typically provided by Django exceptions. Defaults to None.
            non_field_errors (list, optional): List of non-field errors to include as top-level key.

        Returns:
            Response: DRF response object with desired format - can be used directly in views
        """
        api_response = ApiResponse(
            message=message,
            status=status,
            results=results,
            error_fields=error_fields,
            non_field_errors=non_field_errors,
        )
        if response:  # response passed -> simply edit
            api_response.extras = response.data
        return Response(api_response.dict(), status=status)

    def _handle_logging(
        self, msg: str, print_log: bool, exception: Optional[Exception] = None
    ) -> None:
        """Internal function to handle logging for responses handled by this class.

        Args:
            print_log (boolean): Whether or not to actually print the message.
            msg (str): Message to print.
            exception (Exception, optional): Exception object to log with stack trace. Defaults to None.
        """
        if print_log:
            logger = self.logger or DEFAULT_LOGGER
            # Let logging handle stack info automatically - more efficient than inspect.stack()
            if exception is not None:
                logger.error(msg, exc_info=True, stack_info=True)
            else:
                logger.error(msg, stack_info=True)

    def _parse_validation_error_message(
        self,
        error: Optional[Union[str, Exception]] = None,
        error_fields: Optional[Dict[Any, Any]] = None,
    ) -> Optional[str]:
        """
        Helper function to parse validation errors and extract meaningful messages.

        This handles different types of validation errors in order of preference:
        1. Django ValidationError with __all__ field
        2. DRF ValidationError with non_field_errors
        3. IntegrityError messages
        4. String errors (raw string)
        5. First string error from error_fields (recursively, including nested structures)

        Args:
            error: The error object (ValidationError, IntegrityError, etc.)
            error_fields: Dictionary of field-specific errors

        Returns:
            Extracted error message string, or None if no suitable message found
        """

        def _extract_first_string_error(obj: Any) -> Optional[str]:
            """Recursively extract the first string error from nested dicts/lists, including DRF ErrorDetail objects."""
            # DRF's ErrorDetail objects are not always present (if DRF isn't installed),
            # so we import ErrorDetail locally and only check for it if available.
            # This avoids a hard dependency on DRF for users who only use Django.
            try:
                from rest_framework.exceptions import ErrorDetail

                if isinstance(obj, ErrorDetail):
                    return str(obj)
            except ImportError:
                pass
            if isinstance(obj, str):
                return obj
            if isinstance(obj, list):
                for item in obj:
                    result = _extract_first_string_error(item)
                    if result:
                        return result
            if isinstance(obj, dict):
                for value in obj.values():
                    result = _extract_first_string_error(value)
                    if result:
                        return result
            return None

        # Handle Django ValidationError
        if (
            isinstance(error, ValidationError)
            and hasattr(error, "message_dict")
            and "__all__" in error.message_dict
        ):
            message_dict = error.message_dict.get("__all__")
            if isinstance(message_dict, list) and len(message_dict) > 0:
                return str(message_dict[0])

        # Handle DRF ValidationError
        elif isinstance(error, DRFValidationError):
            if hasattr(error, "detail"):
                # Try non_field_errors first if detail is a dict
                if (
                    isinstance(error.detail, dict)
                    and "non_field_errors" in error.detail
                ):
                    non_field_errors = error.detail["non_field_errors"]
                    if isinstance(non_field_errors, list) and len(non_field_errors) > 0:
                        return str(non_field_errors[0])
                # Recursively extract from dict or list
                if isinstance(error.detail, (dict, list)):
                    return _extract_first_string_error(error.detail)
                # Fallback to string representation
                return str(error.detail)

        # Handle IntegrityError
        elif isinstance(error, IntegrityError):
            return str(error)

        # Handle string errors
        elif isinstance(error, str):
            return error

        # Handle other exceptions with string representation
        elif isinstance(error, Exception):
            return str(error)

        # Finally, try to extract from error_fields if available
        elif error_fields and len(error_fields) > 0:
            # Look for non_field_errors first
            if "non_field_errors" in error_fields:
                non_field_errors = error_fields["non_field_errors"]
                if isinstance(non_field_errors, list) and len(non_field_errors) > 0:
                    return str(non_field_errors[0])
            # Otherwise, get the first string error recursively
            return _extract_first_string_error(error_fields)

        return None

    #
    # RESPONSE SUCCESS
    #
    def response_success(
        self,
        message: Optional[str] = None,
        results: Optional[Union[object, Dict[Any, Any], List[Any]]] = None,
        response: Optional[Response] = None,
        status: Optional[int] = HTTP_200_OK,
    ) -> Response:
        """
        :param str message: message to include in response
        :param object results: results object/list to include in response
        :param Response response: response object to simply edit
        :param int status: HTTP status to use

        :returns: response of the desired format
        :rtype: Response
        """
        # no message = use default
        if not message:
            message = self.message_success

        return self._format_response(
            response=response, results=results, message=message, status=status
        )

    #
    # RESPONSE ERROR
    #
    def response_error(
        self,
        error: Optional[Union[str, Exception]] = None,
        error_fields: Optional[Dict[Any, Any]] = None,
        message: Optional[str] = None,
        results: Optional[Union[object, Dict[Any, Any], List[Any]]] = None,
        response: Optional[Response] = None,
        status: Optional[int] = HTTP_400_BAD_REQUEST,
        print_log: Optional[bool] = True,
    ) -> Response:
        """
        :param str|Exception error: error message to log
        :param dict error_fields: list of fields to include in error response
        :param str message: message to include in response
        :param object results: results object/list to include in response
        :param Response response: response object to simply edit
        :param int status: HTTP status to use
        :param bool print_log: override whether to print this error

        :returns: response of the desired format
        :rtype: Response
        """
        # Figure out actual message

        # Initialize message_res with default error message
        message_res = self.message_error

        # if print_log not set, default to True
        if print_log is None:
            print_log = True

        # Priority 1: Use provided message if available (top priority)
        if message:
            message_res = str(message)
        else:
            # Priority 2: Try to parse validation errors for a meaningful message
            parsed_message = self._parse_validation_error_message(error, error_fields)
            if parsed_message:
                message_res = parsed_message

        # Figure out logging / error

        # error PASSED, this means we are potentially logging something
        if error:
            # Only pass exception to logging if it's actually an Exception instance
            exception_for_logging = error if isinstance(error, Exception) else None

            if message and message != error:  # message and error different, log both
                self._handle_logging(
                    f"{message} - {error}", print_log, exception_for_logging
                )
            else:  # error and message both exist and are the same
                self._handle_logging(str(error), print_log, exception_for_logging)
        # if no error, but message exists, log it
        elif message:
            self._handle_logging(message, print_log)

        # Extract non_field_errors from error_fields if present, without mutating input
        non_field_errors = None
        error_fields_copy = None
        if error_fields:
            error_fields_copy = error_fields.copy()
            if "non_field_errors" in error_fields_copy:
                candidate = error_fields_copy.pop("non_field_errors")
                if candidate:  # Only include if truthy (not None, not empty)
                    non_field_errors = candidate
            if not error_fields_copy:
                error_fields_copy = None
        else:
            error_fields_copy = None

        # Handle response
        return self._format_response(
            response=response,
            results=results,
            message=message_res,
            status=status,
            error_fields=error_fields_copy,
            non_field_errors=non_field_errors,
        )
