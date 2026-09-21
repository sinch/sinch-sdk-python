from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.exceptions import (
    NumberNotFoundException,
    NumbersException,
)
from sinch.domains.numbers.api.v1.internal.base import NumbersEndpoint
from sinch.domains.numbers.models.v1.internal import (
    UpdateEventDestinationRequest,
)
from sinch.domains.numbers.models.v1.internal.base.base_model_configuration import (
    BaseModelConfigurationRequest,
)
from sinch.domains.numbers.models.v1.response import (
    EventDestinationResponse,
)


class GetEventDestinationEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/callbackConfiguration"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: BaseModelConfigurationRequest,
        response_model=EventDestinationResponse,
    ):
        super().__init__(project_id, request_data, response_model)

    def handle_response(
        self, response: HTTPResponse
    ) -> EventDestinationResponse:
        try:
            super().handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self._process_response_model(
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
        self,
        project_id: str,
        request_data: UpdateEventDestinationRequest,
        response_model=EventDestinationResponse,
    ):
        super().__init__(project_id, request_data, response_model)

    def handle_response(
        self, response: HTTPResponse
    ) -> EventDestinationResponse:
        try:
            super().handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self._process_response_model(
            response.body, EventDestinationResponse
        )
