from abc import ABC, abstractmethod
from sinch.core.models.http_response import HTTPResponse
from sinch.core.enums import HTTPAuthentication, HTTPMethod


class HTTPEndpoint(ABC):
    ENDPOINT_URL: str
    HTTP_METHOD: HTTPMethod
    HTTP_AUTHENTICATION: HTTPAuthentication

    def __init__(self, project_id, request_data):
        pass

    def build_url(self, sinch) -> str:
        return ''

    def build_query_params(self) -> dict:
        return {}

    def request_body(self) -> dict:
        return {}

    @abstractmethod
    def handle_response(self, response: HTTPResponse):
        pass
