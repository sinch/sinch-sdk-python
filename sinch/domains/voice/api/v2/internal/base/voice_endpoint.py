from abc import ABC

from sinch.core.endpoint import BaseHTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException


class VoiceEndpoint(BaseHTTPEndpoint, ABC):
    def _get_origin(self, sinch) -> str:
        return sinch.configuration.voice_v2_origin

    def _raise_for_error(self, response: HTTPResponse) -> None:
        if response.status_code >= 400:
            error_body = (
                response.body if isinstance(response.body, dict) else {}
            )
            title = error_body.get("title") or ""
            detail = error_body.get("detail") or ""
            parts = [part for part in (title, detail) if part]
            error_message = ": ".join(parts) or f"Error {response.status_code}"
            raise VoiceException(
                message=error_message,
                response=response,
                is_from_server=True,
                error_type=error_body.get("type"),
                instance=error_body.get("instance"),
            )
