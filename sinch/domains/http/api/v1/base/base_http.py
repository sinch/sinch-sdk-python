from typing import Optional, Type

from sinch.core.clients.request_options import RequestOptions
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.http.api.v1.internal import HttpCallEndpoint


class BaseHttp:
    """Base class for handling Sinch HTTP transport operations."""

    def __init__(self, sinch):
        self._sinch = sinch

    def _request(
        self,
        endpoint_class: Type[HttpCallEndpoint],
        request_data: HttpRequest,
        request_options: Optional[RequestOptions] = None,
    ) -> HTTPResponse:
        """
        A helper method to make requests to endpoints.

        :param endpoint_class: The endpoint class to call.
        :type endpoint_class: Type[HttpCallEndpoint]
        :param request_data: The request data to pass to the endpoint.
        :type request_data: HttpRequest
        :param request_options: The options for this request, overriding the client configuration.
        :type request_options: Optional[RequestOptions]

        :returns: The response from the Sinch transport request.
        :rtype: HTTPResponse
        """
        endpoint = endpoint_class(
            project_id=None,
            request_data=request_data,
            request_options=request_options,
        )
        endpoint.set_authentication_method(self._sinch)
        return self._sinch.configuration.transport.request(endpoint)
