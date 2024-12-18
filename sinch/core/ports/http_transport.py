import aiohttp
from abc import ABC, abstractmethod
from platform import python_version
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.signature import Signature
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.exceptions import ValidationException, SinchException
from sinch.core.enums import HTTPAuthentication
from sinch.core.token_manager import TokenState
from sinch import __version__ as sdk_version


class HTTPTransport(ABC):
    def __init__(self, sinch):
        self.sinch = sinch

    @abstractmethod
    def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        pass

    def authenticate(self, endpoint, request_data):
        if endpoint.HTTP_AUTHENTICATION in (HTTPAuthentication.BASIC.value, HTTPAuthentication.OAUTH.value):
            if (
                not self.sinch.configuration.key_id
                or not self.sinch.configuration.key_secret
                or not self.sinch.configuration.project_id
            ):
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
            request_data.headers.update({
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
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
        elif endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.SMS_TOKEN.value:
            if not self.sinch.configuration.sms_api_token or not self.sinch.configuration.service_plan_id:
                raise ValidationException(
                    message=(
                        "sms_api_token and service_plan_id are required by this API. "
                        "Those credentials can be obtained from Sinch portal."
                    ),
                    is_from_server=False,
                    response=None
                )
            request_data.headers.update({
                "Authorization": f"Bearer {self.sinch.configuration.sms_api_token}",
                "Content-Type": "application/json"
            })

        return request_data

    def prepare_request(self, endpoint: HTTPEndpoint) -> HttpRequest:
        protocol = "http://" if self.sinch.configuration.disable_https else "https://"
        url_query_params = endpoint.build_query_params()

        return HttpRequest(
            headers={
                "User-Agent": f"sinch-sdk/{sdk_version} (Python/{python_version()};"
                              f" {self.__class__.__name__};)"
            },
            protocol=protocol,
            url=protocol + endpoint.build_url(self.sinch),
            http_method=endpoint.HTTP_METHOD,
            request_body=endpoint.request_body(),
            query_params=url_query_params,
            auth=()
        )

    @staticmethod
    def deserialize_json_response(response):
        if response.content:
            try:
                response_body = response.json()
            except ValueError as err:
                raise SinchException(
                    message=(
                        "Error while parsing json response.",
                        err.msg
                    ),
                    is_from_server=True,
                    response=response
                )
        else:
            response_body = {}

        return response_body

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
