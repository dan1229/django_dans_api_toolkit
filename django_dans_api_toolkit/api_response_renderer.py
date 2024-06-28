from typing import Any, Dict, Mapping, Optional
from rest_framework.renderers import JSONRenderer

from .api_response_handler import ApiResponseHandler

"""
============================================================================================ #
API RESPONSE RENDERER ====================================================================== #
============================================================================================ #
"""


#
# API Response Renderer class, this overrides the 'default' one used by
# DRF and allows us to validate and edit ALL api responses
#
# This is designed to work in tandem with the Api Response Handler
# but can also be used alone. The default response renderer is in the settings.
#
class ApiResponseRenderer(JSONRenderer):
    def render(
        self,
        data: Dict[Any, Any],
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        # if 'detail' exists, copy it to 'message'
        if data.get("detail"):
            data["message"] = data["detail"]

        # if 'message' does NOT exist, get one just in case
        if not data.get("message"):
            if renderer_context is not None:
                status_code = renderer_context["response"].status_code
                if 200 <= status_code < 300:
                    data["message"] = ApiResponseHandler().message_success
                else:
                    data["message"] = ApiResponseHandler().message_error

        # if 'results' does NOT exist, get one just in case
        if not data.get("results") and data.get("results") != []:
            data["results"] = None

        # if 'error_fields' does NOT exist, get one just in case
        if not data.get("error_fields"):
            data["error_fields"] = None

        return super(ApiResponseRenderer, self).render(
            data, accepted_media_type, renderer_context
        )
