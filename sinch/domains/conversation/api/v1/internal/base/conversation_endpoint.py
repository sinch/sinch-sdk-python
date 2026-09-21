from abc import ABC

from sinch.core.endpoint import BaseHTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException


class ConversationEndpoint(BaseHTTPEndpoint, ABC):
    def _get_origin(self, sinch) -> str:
        return sinch.configuration.get_conversation_origin()

    def _raise_for_error(self, response: HTTPResponse) -> None:
        if response.status_code >= 400:
            error = (response.body or {}).get("error", {})
            message = error.get("message", "")
            status = error.get("status", "")
            error_message = (
                f"{message}  {status}".strip()
                or f"Error {response.status_code}"
            )
            raise ConversationException(
                message=error_message,
                response=response,
                is_from_server=True,
            )
