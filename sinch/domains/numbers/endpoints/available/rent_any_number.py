from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.numbers.models.available.rent_any_number_request import RentAnyNumberRequest
from sinch.domains.numbers.models.available.rent_any_number_response import RentAnyNumberResponse


class RentAnyNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to rent an available virtual number for a project.
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers:rentAny"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: RentAnyNumberRequest):
        super(RentAnyNumberEndpoint, self).__init__(project_id, request_data)

    def handle_response(self, response: HTTPResponse) -> RentAnyNumberResponse:
        """
        Handles the response from the API call.

        Args:
            response (HTTPResponse): The response object from the API call.

        Returns:
            RentAnyNumberResponse: The response data mapped to the RentAnyNumberResponse model.
        """
        super(RentAnyNumberEndpoint, self).handle_response(response)
        return self.process_response_model(response.body, RentAnyNumberResponse)
