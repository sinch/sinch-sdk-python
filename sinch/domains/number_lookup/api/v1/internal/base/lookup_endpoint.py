from abc import ABC
from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.domains.number_lookup.exceptions import NumberLookupException


class LookupEndpoint(HTTPEndpoint, ABC):
    def __init__(self, project_id: str, request_data):
        super().__init__(project_id, request_data)

    def handle_response(self, response: HTTPResponse):
        if response.status_code >= 400:
            error_message = f"Error {response.status_code}"

            raise NumberLookupException(
                message=error_message,
                response=response,
                is_from_server=True,
            )
