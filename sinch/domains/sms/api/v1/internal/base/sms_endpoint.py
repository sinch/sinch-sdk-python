from abc import ABC

from sinch.core.endpoint import BaseHTTPEndpoint
from sinch.core.enums import HTTPAuthentication
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.exceptions import SmsException


class SmsEndpoint(BaseHTTPEndpoint, ABC):
    UNSET_SERIALIZATION: bool = False

    def set_authentication_method(self, sinch):
        """
        Sets the authentication method based on the sinch client configuration.
        """
        if sinch.configuration.authentication_method == "sms_auth":
            self.HTTP_AUTHENTICATION = HTTPAuthentication.SMS_TOKEN.value
        else:
            self.HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def _get_origin(self, sinch) -> str:
        return sinch.configuration.get_sms_origin_for_auth()

    def _raise_for_error(self, response: HTTPResponse) -> None:
        if response.status_code >= 400:
            raise SmsException(
                message=f"Error {response.status_code}",
                response=response,
                is_from_server=True,
            )
