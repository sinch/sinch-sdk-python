from abc import ABC, abstractmethod
from sinch.core.models.http_response import HTTPResponse


class HTTPEndpoint(ABC):
    ENDPOINT_URL = None
    HTTP_METHOD = None
    HTTP_AUTHENTICATION = None

    def __init__(self, project_id, request_data):
        pass

    def get_url_without_origin(self, sinch):
        return '/' + '/'.join(self.build_url(sinch).split('/')[1:])

    def build_url(self, sinch):
        return

    def build_query_params(self):
        pass

    def request_body(self):
        return

    @abstractmethod
    def handle_response(self, response: HTTPResponse):
        pass
