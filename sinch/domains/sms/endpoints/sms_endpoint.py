from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.domains.sms.exceptions import SMSException


class SMSEndpoint(HTTPEndpoint):
    def handle_response(self, response: HTTPResponse):
        if response.status_code >= 400:
            raise SMSException(
                message=response.body["text"],
                response=response,
                is_from_server=True
            )
