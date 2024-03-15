from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.domains.voice.exceptions import VoiceException


class VoiceEndpoint(HTTPEndpoint):
    def handle_response(self, response: HTTPResponse):
        if response.status_code >= 400:
            raise VoiceException(
                message=response.body["message"],
                response=response,
                is_from_server=True
            )
