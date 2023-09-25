import aiohttp
import json
from sinch.core.ports.http_transport import AsyncHTTPTransport, HttpRequest
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse


class HTTPTransportAioHTTP(AsyncHTTPTransport):
    async def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        request_data: HttpRequest = self.prepare_request(endpoint)
        request_data_with_auth: HttpRequest = await self.authenticate(endpoint, request_data)

        self.sinch.configuration.logger.debug(
            f"Async HTTP {request_data_with_auth.http_method} call with headers:"
            f" {request_data_with_auth.headers} and body: {request_data_with_auth.request_body}"
            f" to URL: {request_data_with_auth.url}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=request_data_with_auth.http_method,
                headers=request_data_with_auth.headers,
                url=request_data_with_auth.url,
                data=request_data_with_auth.request_body,
                auth=request_data_with_auth.auth,
                params=request_data_with_auth.query_params,
                timeout=aiohttp.ClientTimeout(
                    total=self.sinch.configuration.connection_timeout
                )
            ) as response:

                response_body = await response.read()
                if response_body:
                    response_body = json.loads(response_body)

                self.sinch.configuration.logger.debug(
                    f"Async HTTP {response.status} response with headers: {response.headers}"
                    f"and body: {response_body} from URL: {request_data_with_auth.url}"
                )

                return await self.handle_response(
                    endpoint=endpoint,
                    http_response=HTTPResponse(
                        status_code=response.status,
                        body=response_body,
                        headers=response.headers
                    )
                )
