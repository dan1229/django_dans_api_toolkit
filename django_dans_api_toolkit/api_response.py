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

    status: int
    message: Optional[str]
    results: Optional[Union[object, Dict[Any, Any], List[Any]]]
    error_fields: Optional[Dict[Any, Any]]
    non_field_errors: Optional[List[Any]]
    extras: Union[Dict[Any, Any], object]

    def __init__(
        self,
        status: Optional[int] = None,
        message: Optional[str] = None,
        results: Optional[Union[object, Dict[Any, Any], List[Any]]] = None,
        error_fields: Optional[Dict[Any, Any]] = None,
        non_field_errors: Optional[List[Any]] = None,
        **kwargs: Any
    ) -> None:
        if not status:
            # if status is not provided, we assume error
            status = 400
        self.status = status
        self.message = message
        self.results = results
        self.error_fields = error_fields
        self.non_field_errors = non_field_errors
        # Merge extras dict into kwargs if present
        extras = kwargs.pop("extras", None)
        if isinstance(extras, dict):
            kwargs.update(extras)
        self.extras = kwargs

    def dict(self) -> Dict[Any, Any]:
        """
        Convert ApiResponse to dict. Primarily to use in actual Response object.

        - For paginated DRF responses (dicts with 'count', 'next', 'previous', 'results'),
          merges those keys into the top-level dict alongside custom fields.
        - For non-paginated responses, uses the standard structure.

        :returns: Dict containing ApiResponse object info
        :rtype: dict
        """
        res: Dict[Any, Any]
        # If results is a paginated DRF response, merge those keys at the top level
        if isinstance(self.results, dict) and set(
            ["count", "next", "previous", "results"]
        ).issubset(self.results.keys()):
            res = {
                "status": self.status,
                "message": self.message,
                **{
                    k: self.results[k] for k in ["count", "next", "previous", "results"]
                },
            }
        else:
            res = {
                "status": self.status,
                "message": self.message,
                "results": self.results,
            }
        # Add error_fields, non_field_errors, and extras in both cases
        res["error_fields"] = self.error_fields if self.error_fields else None
        if self.non_field_errors:
            res["non_field_errors"] = self.non_field_errors
        if self.extras:
            res["extras"] = self.extras
        return res
