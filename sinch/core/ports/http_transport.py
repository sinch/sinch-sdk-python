import aiohttp
from abc import ABC
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.signature import Signature
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.exceptions import ValidationException
from sinch.core.enums import HTTPAuthentication
from sinch.core.token_manager import TokenState


class HTTPTransport(ABC):
    def __init__(self, sinch):
        self.sinch = sinch

    def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        pass

    def authenticate(self, endpoint, request_data):
        if endpoint.HTTP_AUTHENTICATION in (HTTPAuthentication.BASIC.value, HTTPAuthentication.OAUTH.value):
            if not self.sinch.configuration.key_id or not self.sinch.configuration.key_secret or not self.sinch.configuration.project_id:
                raise ValidationException(
                    message=(
                        "key_id, key_secret and project_id are required by this API. "
                        "Those credentials can be obtained from Sinch portal."
                    ),
                    is_from_server=False,
                    response=None
                )

        if endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.BASIC.value:
            request_data.auth = (self.sinch.configuration.key_id, self.sinch.configuration.key_secret)
        else:
            request_data.auth = None

        if endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.OAUTH.value:
            token = self.sinch.authentication.get_auth_token().access_token
            request_data.headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        elif endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.SIGNED.value:
            if not self.sinch.configuration.application_key or not self.sinch.configuration.application_secret:
                raise ValidationException(
                    message=(
                        "application key and application secret are required by this API. "
                        "Those credentials can be obtained from Sinch portal."
                    ),
                    is_from_server=False,
                    response=None
                )
            signature = Signature(
                self.sinch,
                endpoint.HTTP_METHOD,
                request_data.request_body,
                endpoint.get_url_without_origin(self.sinch)
            )
            request_data.headers = signature.get_http_headers_with_signature()

        return request_data

    def prepare_request(self, endpoint: HTTPEndpoint) -> HttpRequest:
        protocol = "http://" if self.sinch.configuration.disable_https else "https://"
        url_query_params = endpoint.build_query_params()

        return HttpRequest(
            headers={},
            protocol=protocol,
            url=protocol + endpoint.build_url(self.sinch),
            http_method=endpoint.HTTP_METHOD,
            request_body=endpoint.request_body(),
            query_params=url_query_params,
            auth=()
        )

    def handle_response(self, endpoint: HTTPEndpoint, http_response: HTTPResponse):
        if http_response.status_code == 401 and endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.OAUTH.value:
            self.sinch.configuration.token_manager.handle_invalid_token(http_response)
            if self.sinch.configuration.token_manager.token_state == TokenState.EXPIRED:
                return self.request(endpoint=endpoint)

        return endpoint.handle_response(http_response)


class AsyncHTTPTransport(HTTPTransport):
    async def authenticate(self, endpoint, request_data):
        if endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.BASIC.value:
            request_data.auth = aiohttp.BasicAuth(
                self.sinch.configuration.key_id,
                self.sinch.configuration.key_secret
            )
        else:
            request_data.auth = None

        if endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.OAUTH.value:
            token_response = await self.sinch.authentication.get_auth_token()
            request_data.headers = {
                "Authorization": f"Bearer {token_response.access_token}",
                "Content-Type": "application/json"
            }

        return request_data

    async def handle_response(self, endpoint: HTTPEndpoint, http_response: HTTPResponse):
        if http_response.status_code == 401 and endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.OAUTH.value:
            self.sinch.configuration.token_manager.handle_invalid_token(http_response)
            if self.sinch.configuration.token_manager.token_state == TokenState.EXPIRED:
                return await self.request(endpoint=endpoint)

        return endpoint.handle_response(http_response)
