import json
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.exceptions import (
    NumbersException,
    NumberNotFoundException,
)
from sinch.domains.numbers.api.v1.internal.base import NumbersEndpoint
from sinch.domains.numbers.models.v1.internal import (
    UpdateEventDestinationRequest,
)
from sinch.domains.numbers.models.v1.response import (
    EventDestinationResponse,
)


class GetEventDestinationEndpoint(NumbersEndpoint):
    """
    Endpoint to get the event destination configuration for a project.
    """

    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/callbackConfiguration"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data=None):
        super(GetEventDestinationEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        if self.request_data:
            super(GetEventDestinationEndpoint, self).build_url(sinch)
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id,
        )

    def build_query_params(self) -> dict:
        if self.request_data:
            return self.request_data.model_dump(
                exclude_none=True, by_alias=True
            )
        return {}

    def handle_response(
        self, response: HTTPResponse
    ) -> EventDestinationResponse:
        try:
            super(GetEventDestinationEndpoint, self).handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(
            response.body, EventDestinationResponse
        )


class UpdateEventDestinationEndpoint(NumbersEndpoint):
    """
    Endpoint to update the event destination configuration for a project.
    """

    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/callbackConfiguration"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self, project_id: str, request_data: UpdateEventDestinationRequest
    ):
        super(UpdateEventDestinationEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        request_data = self.request_data.model_dump(
            by_alias=True, exclude_none=True
        )
        return json.dumps(request_data)

    def handle_response(
        self, response: HTTPResponse
    ) -> EventDestinationResponse:
        try:
            super(UpdateEventDestinationEndpoint, self).handle_response(
                response
            )
        except NumbersException as e:
            raise NumberNotFoundException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(
            response.body, EventDestinationResponse
        )
