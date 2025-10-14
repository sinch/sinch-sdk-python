from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.domains.verification.exceptions import VerificationException


class VerificationEndpoint(HTTPEndpoint):
    def handle_response(self, response: HTTPResponse):
        if response.status_code >= 400:
            raise VerificationException(message=response.body["message"], response=response, is_from_server=True)
