from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.domains.numbers.exceptions import NumbersException


class NumbersEndpoint(HTTPEndpoint):
    def handle_response(self, response: HTTPResponse):
        if response.status_code >= 400:
            raise NumbersException(
                message=response.body["error"].get("message"),
                response=response,
                is_from_server=True
            )
