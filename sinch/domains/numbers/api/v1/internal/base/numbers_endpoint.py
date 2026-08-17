from abc import ABC

from sinch.core.endpoint import BaseHTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.exceptions import NumbersException
from sinch.domains.numbers.models.v1.errors import NotFoundError


class NumbersEndpoint(BaseHTTPEndpoint, ABC):
    UNSET_SERIALIZATION: bool = False

    def _get_origin(self, sinch) -> str:
        return sinch.configuration.numbers_origin

    def _raise_for_error(self, response: HTTPResponse) -> None:
        error_data = (response.body or {}).get("error", {})

        if response.status_code == 404:
            try:
                error = NotFoundError(**error_data)
            except TypeError:
                error = f"Not found: {error_data}"
            raise NumbersException(
                message=error, response=response, is_from_server=True
            )

        if response.status_code >= 400:
            message = error_data.get("message", "")
            status = error_data.get("status", "")
            error_message = (
                f"{message}  {status}".strip()
                or f"Error {response.status_code}"
            )
            raise NumbersException(
                message=error_message,
                response=response,
                is_from_server=True,
            )
