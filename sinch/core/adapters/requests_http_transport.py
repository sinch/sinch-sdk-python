import requests
import json
from typing import cast
from sinch.core.ports.http_transport import HTTPTransport, HttpRequest
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.core.clients.sinch_client_base import ClientBase
from sinch.core.models.base_model import SinchBaseModel


class HTTPTransportRequests(HTTPTransport):
    def __init__(self, sinch: ClientBase):
        super().__init__(sinch)
        self.http_session = requests.Session()

    def request(self, endpoint: HTTPEndpoint) -> SinchBaseModel:
        request_data: HttpRequest = self.prepare_request(endpoint)
        request_data_with_auth = cast(HttpRequest, self.authenticate(endpoint, request_data))

        self.sinch.configuration.logger.debug(
            f"Sync HTTP {request_data_with_auth.http_method} call with headers:"
            f" {request_data_with_auth.headers} and body: {request_data_with_auth.request_body}"
            f"to URL: {request_data_with_auth.url}"
        )

        response = self.http_session.request(
            method=request_data.http_method,
            url=request_data.url,
            data=request_data.request_body,
            auth=request_data.auth,
            headers=request_data.headers,
            timeout=self.sinch.configuration.connection_timeout,
            params=request_data_with_auth.query_params
        )

        response_body = {}
        if response.content:
            response_body = json.loads(response.content)

        self.sinch.configuration.logger.debug(
            f"Sync HTTP {response.status_code} response with headers: {response.headers}"
            f"and body: {response_body} from URL: {request_data_with_auth.url}"
        )

        return cast(SinchBaseModel, self.handle_response(
            endpoint=endpoint,
            http_response=HTTPResponse(
                status_code=response.status_code,
                body=response_body,
                headers=dict(response.headers)
            )
        ))
