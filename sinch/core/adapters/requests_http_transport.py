import requests
import json
from sinch.core.ports.http_transport import HTTPTransport, HttpRequest
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse


class HTTPTransportRequests(HTTPTransport):
    def __init__(self, sinch):
        super().__init__(sinch)
        self.http_session = requests.Session()

    def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        request_data: HttpRequest = self.prepare_request(endpoint)
        request_data: HttpRequest = self.authenticate(endpoint, request_data)

        self.sinch.configuration.logger.debug(
            f"Sync HTTP {request_data.http_method} call with headers:"
            f" {request_data.headers} and body: {request_data.request_body} to URL: {request_data.url}"
        )

        response = self.http_session.request(
            method=request_data.http_method,
            url=request_data.url,
            data=request_data.request_body,
            auth=request_data.auth,
            headers=request_data.headers,
            timeout=self.sinch.configuration.connection_timeout,
            params=request_data.query_params
        )

        response_body = response.content
        if response_body:
            response_body = json.loads(response_body)

        self.sinch.configuration.logger.debug(
            f"Sync HTTP {response.status_code} response with headers: {response.headers}"
            f"and body: {response_body} from URL: {request_data.url}"
        )

        return self.handle_response(
            endpoint=endpoint,
            http_response=HTTPResponse(
                status_code=response.status_code,
                body=response_body,
                headers=response.headers
            )
        )
