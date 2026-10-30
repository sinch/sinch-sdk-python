import requests
from sinch.core.ports.http_transport import HTTPTransport, HttpRequest
from sinch.core.models.http_headers import HttpHeaders
from sinch.core.models.http_content import HttpContent
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
        url = request_data.url + request_data.query_parameters
        body_text = request_data.content.as_string(errors="replace") if request_data.content is not None else None
        self.sinch.configuration.logger.debug(
            "Sync HTTP request %r with body: %s",
            request_data, body_text
        )
        response = self.http_session.request(
            method=request_data.method,
            url=url,
            data=request_data.content.as_bytes() if request_data.content is not None else None,
            headers=request_data.headers,
            timeout=self.sinch.configuration.transport_settings.timeout_seconds or None,
        )

        http_response = HTTPResponse(
            status=response.status_code,
            headers=HttpHeaders(response.raw.headers),
            content=response.content,
        )

        self.sinch.configuration.logger.debug(
            "Sync HTTP response %r with body: %s from URL: %s",
            http_response, http_response.content.as_string(errors="replace"), url
        )

        return http_response
