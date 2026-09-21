from abc import ABC

from sinch.core.endpoint import BaseHTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.number_lookup.exceptions import NumberLookupException


class LookupEndpoint(BaseHTTPEndpoint, ABC):
    UNSET_SERIALIZATION: bool = False

    def _get_origin(self, sinch) -> str:
        return sinch.configuration.number_lookup_origin

    def _raise_for_error(self, response: HTTPResponse) -> None:
        if response.status_code >= 400:
            raise NumberLookupException(
                message=f"Error {response.status_code}",
                response=response,
                is_from_server=True,
            )
