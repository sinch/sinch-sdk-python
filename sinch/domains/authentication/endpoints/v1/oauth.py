from sinch.core.clients.request_options import RequestOptions
from sinch.core.models.http_body import UrlEncodedBody
from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.authentication.exceptions import AuthenticationException
from sinch.domains.authentication.models.v1.authentication import OAuthToken


class OAuthEndpoint(HTTPEndpoint):
    ENDPOINT_URL = "{origin}/oauth2/token"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.BASIC.value
    # The token is only requested when Sinch authentication is enabled for a request
    request_options = RequestOptions(use_sinch_auth=True)

    def __init__(self):
        pass

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.auth_origin
        )

    def build_body(self) -> UrlEncodedBody:
        return UrlEncodedBody({
            "grant_type": "client_credentials"
        })

    def handle_response(self, response: HTTPResponse):
        body = response.content.as_json() or {}
        if response.status >= 400:
            raise AuthenticationException(
                message=body.get("error_description"),
                response=response,
                is_from_server=True
            )
        else:
            return OAuthToken(
                access_token=body["access_token"],
                expires_in=body["expires_in"],
                scope=body["scope"],
                token_type=body["token_type"]
            )
