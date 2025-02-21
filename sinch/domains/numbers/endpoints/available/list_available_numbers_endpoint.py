from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.domains.numbers.models.available.list_available_numbers_request import ListAvailableNumbersRequest
from sinch.domains.numbers.models.available.list_available_numbers_response import ListAvailableNumbersResponse
from sinch.domains.numbers.models.numbers import Number


class AvailableNumbersEndpoint(NumbersEndpoint):
    """
    Endpoint to list available virtual numbers for a project.
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListAvailableNumbersRequest):
        super(AvailableNumbersEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data

    def build_query_params(self) -> dict:
        return self.request_data.model_dump(exclude_none=True, by_alias=True)

    def handle_response(self, response: HTTPResponse) -> list[Number]:
        """
        Processes the API response and maps it to a response model.

        Args:
            response (HTTPResponse): The raw HTTP response object received from the API.

        Returns:
            list[Number]: The response model containing the parsed response data.
        """
        super(AvailableNumbersEndpoint, self).handle_response(response)
        response = self.process_response_model(response.body, ListAvailableNumbersResponse)
        return response.available_numbers
