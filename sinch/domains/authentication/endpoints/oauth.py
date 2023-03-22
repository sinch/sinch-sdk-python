from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.authentication.exceptions import AuthenticationException
from sinch.domains.authentication.models.authentication import OAuthToken


class OAuthEndpoint(HTTPEndpoint):
    ENDPOINT_URL = "{origin}/oauth2/token"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.BASIC.value

    def __init__(self):
        pass

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.auth_origin
        )

    def request_body(self) -> dict:
        return {
            "grant_type": "client_credentials"
        }

    def handle_response(self, response: HTTPResponse):
        if response.status_code >= 400:
            raise AuthenticationException(
                message=response.body.get("error_description"),
                response=response,
                is_from_server=True
            )
        else:
            return OAuthToken(
                access_token=response.body["access_token"],
                expires_in=response.body["expires_in"],
                scope=response.body["scope"],
                token_type=response.body["token_type"]
            )
