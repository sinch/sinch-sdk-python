from abc import ABC

from sinch.core.endpoint import HTTPEndpoint
from sinch.core.enums import HTTPAuthentication
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.http.api.v1.exceptions import HttpException


class HttpEndpoint(HTTPEndpoint, ABC):
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def set_authentication_method(self, sinch) -> None:
        """
        Sets the authentication method from the sinch client configuration: OAuth when the access key is
        configured, as it is accepted by every Sinch API, the SMS API token otherwise.
        """
        configuration = sinch.configuration
        if configuration.key_id and configuration.key_secret:
            self.HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value
        elif configuration.service_plan_id and configuration.sms_api_token:
            self.HTTP_AUTHENTICATION = HTTPAuthentication.SMS_TOKEN.value
        else:
            self.HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def _raise_for_error(self, response: HTTPResponse) -> None:
        if response.status >= 400:
            raise HttpException(
                message=f"Error {response.status}",
                response=response,
                is_from_server=True,
            )

    def handle_response(self, response: HTTPResponse) -> HTTPResponse:
        self._raise_for_error(response)
        return response
