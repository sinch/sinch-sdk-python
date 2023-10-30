from abc import ABC, abstractmethod
from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.base_model import SinchBaseModel, SinchRequestBaseModel
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sinch.core.clients.sinch_client_base import ClientBase


class HTTPEndpoint(ABC):
    ENDPOINT_URL: str
    HTTP_METHOD: HTTPMethod
    HTTP_AUTHENTICATION: HTTPAuthentication
    project_id: str
    request_data: SinchRequestBaseModel

    def __init__(self, project_id: str, request_data: SinchRequestBaseModel):
        pass

    def build_url(self, sinch: 'ClientBase') -> str:
        return ''

    def build_query_params(self) -> dict:
        return {}

    def request_body(self) -> dict:
        return {}

    @abstractmethod
    def handle_response(self, response: HTTPResponse) -> SinchBaseModel:
        pass
