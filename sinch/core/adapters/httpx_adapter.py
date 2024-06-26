import httpx
from sinch.core.ports.http_transport import AsyncHTTPTransport, HttpRequest
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse


class HTTPXTransport(AsyncHTTPTransport):
    def __init__(self, sinch):
        super().__init__(sinch)
        self.http_session = None

    async def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        request_data: HttpRequest = self.prepare_request(endpoint)
        request_data: HttpRequest = await self.authenticate(endpoint, request_data)

        if not self.http_session:
            self.http_session = httpx.AsyncClient()

        self.sinch.configuration.logger.debug(
            f"Async HTTP {request_data.http_method} call with headers:"
            f" {request_data.headers} and body: {request_data.request_body} to URL: {request_data.url}"
        )

        if isinstance(request_data.request_body, str):
            response = await self.http_session.request(
                method=request_data.http_method,
                headers=request_data.headers,
                url=request_data.url,
                content=request_data.request_body,
                auth=request_data.auth,
                params=request_data.query_params
            )
        else:
            response = await self.http_session.request(
                method=request_data.http_method,
                headers=request_data.headers,
                url=request_data.url,
                data=request_data.request_body,
                auth=request_data.auth,
                params=request_data.query_params
            )

        if response.content:
            response_body = response.json()
        else:
            response_body = {}

        self.sinch.configuration.logger.debug(
            f"Async HTTP {response.status_code} response with headers: {response.headers}"
            f"and body: {response_body} from URL: {request_data.url}"
        )

        return await self.handle_response(
            endpoint=endpoint,
            http_response=HTTPResponse(
                status_code=response.status_code,
                body=response_body,
                headers=response.headers
            )
        )
