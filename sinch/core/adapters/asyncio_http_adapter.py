import aiohttp
import json
from sinch.core.ports.http_transport import AsyncHTTPTransport, HttpRequest
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse


class HTTPTransportAioHTTP(AsyncHTTPTransport):
    def __init__(self, sinch):
        super().__init__(sinch)
        self.http_session = None

    async def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        request_data: HttpRequest = self.prepare_request(endpoint)
        request_data: HttpRequest = await self.authenticate(endpoint, request_data)

        if not self.http_session:
            self.http_session = aiohttp.ClientSession()

        self.sinch.configuration.logger.debug(
            f"Async HTTP {request_data.http_method} call with headers:"
            f" {request_data.headers} and body: {request_data.request_body} to URL: {request_data.url}"
        )

        async with self.http_session.request(
            method=request_data.http_method,
            headers=request_data.headers,
            url=request_data.url,
            data=request_data.request_body,
            auth=request_data.auth,
            params=request_data.query_params,
            timeout=aiohttp.ClientTimeout(
                total=self.sinch.configuration.connection_timeout
            )
        ) as response:

            response_body = await response.read()
            if response_body:
                response_body = json.loads(response_body)

            self.sinch.configuration.logger.debug(
                f"Async HTTP {response.status} response with headers: {response.headers}"
                f"and body: {response_body} from URL: {request_data.url}"
            )

            return await self.handle_response(
                endpoint=endpoint,
                http_response=HTTPResponse(
                    status_code=response.status,
                    body=response_body,
                    headers=response.headers
                )
            )
