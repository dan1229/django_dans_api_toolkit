from typing import Optional, Dict, List, Union

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
    results: Optional[Union[Dict[str, object], List[object]]]
    error_fields: Optional[Dict[str, List[str]]]
    non_field_errors: Optional[List[str]]
    extras: Optional[Dict[str, object]]

    def __init__(
        self,
        status: Optional[int] = None,
        message: Optional[str] = None,
        results: Optional[Union[Dict[str, object], List[object]]] = None,
        error_fields: Optional[Dict[str, List[str]]] = None,
        non_field_errors: Optional[Union[str, List[str]]] = None,
        **kwargs: object
    ) -> None:
        if not status:
            # if status is not provided, we assume error
            status = 400
        self.status = status
        self.message = message
        self.results = results
        self.error_fields = error_fields
        # Always store non_field_errors as a list if provided
        if isinstance(non_field_errors, str):
            self.non_field_errors = [non_field_errors]
        else:
            self.non_field_errors = non_field_errors
        # Merge extras dict into kwargs if present
        extras = kwargs.pop("extras", None)
        if isinstance(extras, dict):
            kwargs.update(extras)
        self.extras = kwargs

    def dict(self) -> Dict[str, Optional[object]]:
        """
        Convert ApiResponse to dict. Primarily to use in actual Response object.

        - For paginated DRF responses (dicts with 'count', 'next', 'previous', 'results'),
          merges those keys into the top-level dict alongside custom fields.
        - For non-paginated responses, uses the standard structure.

        :returns: Dict containing ApiResponse object info
        :rtype: dict
        """
        res: Dict[str, Optional[object]]
        # If results is a paginated DRF response, merge those keys at the top level
        if isinstance(self.results, dict) and set(
            ["count", "next", "previous", "results"]
        ).issubset(self.results.keys()):
            res = {
                "status": self.status,
                "message": self.message,
                "count": self.results["count"],
                "next": self.results["next"],
                "previous": self.results["previous"],
                "results": self.results["results"],
            }
        else:
            res = {
                "status": self.status,
                "message": self.message,
                "results": self.results,
            }
        # Add error_fields, non_field_errors, and extras in both cases
        res["error_fields"] = (
            self.error_fields if self.error_fields is not None else None
        )
        if self.non_field_errors is not None:
            res["non_field_errors"] = self.non_field_errors
        if self.extras:
            res["extras"] = self.extras
        return res
