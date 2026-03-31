from abc import ABC, abstractmethod
from sinch.core.models.http_response import HTTPResponse


class HTTPEndpoint(ABC):
    ENDPOINT_URL = None

    @property
    @abstractmethod
    def HTTP_METHOD(self) -> str:
        pass

    @property
    @abstractmethod
    def HTTP_AUTHENTICATION(self) -> str:
        pass

    def __init__(self, project_id, request_data):
        self.project_id = project_id
        self.request_data = request_data

    def get_url_without_origin(self, sinch):
        return '/' + '/'.join(self.build_url(sinch).split('/')[1:])

    def build_url(self, sinch):
        return

    def build_query_params(self):
        """
        Constructs the query parameters for the endpoint.

        Returns:
            dict: The query parameters to be sent with the API request.
        """
        pass

    def request_body(self):
        return

    @abstractmethod
    def handle_response(self, response: HTTPResponse):
        pass
