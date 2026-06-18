import requests
from sinch.core.ports.http_transport import HTTPTransport, HttpRequest
from sinch.core.models.http_response import HTTPResponse

class HTTPTransportRequests(HTTPTransport):
    """
    Sync HTTP transport using the requests library.
    """

    def __init__(self, sinch):
        super().__init__(sinch)
        self.http_session = requests.Session()

    def send_request(self, request_data: HttpRequest) -> HTTPResponse:
        """
        Performs the HTTP call with requests and maps the result to an HTTPResponse.

        :param request_data: The prepared request to send.
        :type request_data: HttpRequest
        :returns: The HTTP response.
        :rtype: HTTPResponse
        """
        self.sinch.configuration.logger.debug(
            "Sync HTTP request %s %s",
            request_data.http_method,
            request_data.url
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

        response_body = self.deserialize_json_response(response)

        self.sinch.configuration.logger.debug(
            "Sync HTTP response %s",
            response.status_code
        )

        return HTTPResponse(
            status_code=response.status_code,
            body=response_body,
            headers=response.headers
        )
