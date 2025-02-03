from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.domains.numbers.models.available.activate_number_request import ActivateNumberRequest
from sinch.domains.numbers.models.available.activate_number_response import ActivateNumberResponse


class ActivateNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to activate a virtual number for a project.
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers/{phone_number}:rent"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ActivateNumberRequest):
        super(ActivateNumberEndpoint, self).__init__(project_id, request_data)

    def build_url(self, sinch) -> str:
        """
        Constructs the full URL for the endpoint by formatting the placeholders with actual values.

        Args:
            sinch (Sinch): The Sinch client instance containing configuration details like the API origin.

        Returns:
            str: The fully constructed URL for this API call.
        """
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id,
            phone_number=self.request_data.phone_number
        )

    def handle_response(self, response: HTTPResponse) -> ActivateNumberResponse:
        return self.process_response_model(response.body, ActivateNumberResponse)
