from typing import Optional

from sinch.core.clients.request_options import RequestOptions
from sinch.core.models.http_request import HttpRequest
from sinch.domains.http.api.v1.internal.base import HttpEndpoint


class HttpCallEndpoint(HttpEndpoint):
    USER_AGENT_TAG = "http"

    def __init__(
        self,
        project_id: Optional[str],
        request_data: HttpRequest,
        request_options: Optional[RequestOptions] = None,
    ) -> None:
        super().__init__(project_id, request_data)
        self.request_data: HttpRequest = request_data
        self.request_options = request_options

    @property
    def ENDPOINT_URL(self) -> str:
        return self.request_data.url

    @property
    def HTTP_METHOD(self) -> str:
        return self.request_data.method

    def build_url(self, sinch) -> str:
        return self.request_data.url

    def build_request(self, sinch) -> HttpRequest:
        return self.request_data
