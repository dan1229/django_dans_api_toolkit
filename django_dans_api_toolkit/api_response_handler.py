from typing import Any, Dict, List, Optional, Union
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import logging
import inspect

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
    ) -> Response:
        """Internal function to format responses.

        Args:
            response (Response): Existing DRF response object to use for response.
            results (list): List of results to include in response.
            message (str): Message to include in response.
            status (int): Status to use in response.
            error_fields (dict, optional): Dictionary of field errors to include - typically provided by Django exceptions. Defaults to None.

        Returns:
            Response: DRF response object with desired format - can be used directly in views
        """
        api_response = ApiResponse(
            message=message, status=status, results=results, error_fields=error_fields
        )
        if response:  # response passed -> simply edit
            api_response.extras = response.data
        return Response(api_response.dict(), status=status)

    def _handle_logging(self, msg: str, print_log: bool) -> None:
        """Internal function to handle logging for responses handled by this class.

        Args:
            print_log (boolean): Whether or not to actually print the message.
            msg (str): Message to print.
        """
        if print_log:
            caller_frame = inspect.stack()[2]
            caller_info = f"{caller_frame.filename}:{caller_frame.lineno} in {caller_frame.function}"
            full_msg = f"{msg} | {caller_info}"
            self.logger.error(full_msg)

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

        # use provided message if available
        # this is top priority
        if message:
            message_res = str(message)
        # django validation error
        elif (
            isinstance(error, ValidationError)
            and hasattr(error, "error_dict")
            and error.error_dict.get("__all__")
        ):
            # try to parse ValidationError
            message_dict = error.message_dict.get("__all__")
            if isinstance(message_dict, list) and len(message_dict) > 0:
                message_res = str(message_dict[0])
        # integrity error
        elif isinstance(error, IntegrityError):
            message_res = str(error)
        # get field error for 'message'
        elif error_fields and len(error_fields) > 0:
            # Assuming the first field error is representative
            first_key = next(iter(error_fields))
            first_error_list = error_fields[first_key]
            if isinstance(first_error_list, list) and len(first_error_list) > 0:
                message_res = str(first_error_list[0])

        # Figure out logging / error

        # error PASSED, this means we are potentially logging something
        if error:
            if message and message != error:  # message and error different, log both
                self._handle_logging(f"{message} - {error}", print_log)
            else:  # error and message both exist and are the same
                self._handle_logging(str(error), print_log)
        # if no error, but message exists, log it
        elif message:
            self._handle_logging(message, print_log)

        # Handle response
        return self._format_response(
            response=response,
            results=results,
            message=message_res,
            status=status,
            error_fields=error_fields,
        )
