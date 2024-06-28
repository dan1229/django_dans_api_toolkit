from typing import Any, Optional, Union, Dict, List

"""
============================================================================================ #
API RESPONSE =============================================================================== #
============================================================================================ #
"""


class ApiResponse:
    """
    Response type to standardize response structure and conversions.

    The point of this class is to standardize the response format for all API responses.
    It does so by having properties that model the response structure you'd like.
    """

    def __init__(
        self,
        status: Optional[int] = None,
        message: Optional[str] = None,
        results: Optional[Union[object, Dict[Any, Any], List[Any]]] = None,
        error_fields: Optional[Dict[Any, Any]] = None,
        **kwargs: Any
    ) -> None:
        self.status = status
        self.message = message
        self.results = results
        self.error_fields = error_fields
        self.extras = kwargs

    def dict(self) -> Dict[Any, Any]:
        """
        Convert ApiResponse to dict. Primarily to use in actual Response object.

        :returns: Dict containing ApiResponse object info
        :rtype: dict
        """
        res = {
            "status": self.status,
            "message": self.message,
            "results": self.results,
            "error_fields": self.error_fields,
        }
        for key, value in self.extras.items():
            res[key] = value
        return res
