from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.numbers.models.available.check_number_availability_response import CheckNumberAvailabilityResponse
from sinch.domains.numbers.models.available.check_number_availability_request import CheckNumberAvailabilityRequest


class SearchForNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to check the availability of a virtual number for a project.
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers/{phone_number}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: CheckNumberAvailabilityRequest):
        super(SearchForNumberEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        """
        Constructs the full URL for the endpoint by formatting the placeholders with actual values.
        """
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id,
            phone_number=self.request_data.phone_number
        )

    def handle_response(self, response: HTTPResponse) -> CheckNumberAvailabilityResponse:
        """
        Processes the API response and maps it to a response

        Args:
            response (HTTPResponse): The raw HTTP response object received from the API.

        Returns:
            CheckNumberAvailabilityResponse: The response model containing the parsed response data
            of the requested phone number.
        """
        return self.process_response_model(response.body, CheckNumberAvailabilityResponse)
