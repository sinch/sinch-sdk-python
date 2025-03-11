import json
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.models.v1 import (
    AvailableNumber, CheckNumberAvailabilityResponse, ListAvailableNumbersResponse,
    RentAnyNumberResponse)
from sinch.domains.numbers.models.v1.active_number import ActiveNumber

from sinch.domains.numbers.numbers_endpoint import NumbersEndpoint
from sinch.domains.numbers.exceptions import NumberNotFoundException, NumbersException
from sinch.domains.numbers.models.v1.internal import (
    ActivateNumberRequest, CheckNumberAvailabilityRequest, ListAvailableNumbersRequest, RentAnyNumberRequest
)


class ActivateNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to activate a virtual number for a project.
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers/{phone_number}:rent"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ActivateNumberRequest):
        super(ActivateNumberEndpoint, self).__init__(project_id, request_data)

    def request_body(self) -> str:
        # Convert the request data to a dictionary and remove None values
        request_data = self.request_data.model_dump(by_alias=True, exclude_none=True)
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> ActiveNumber:
        try:
            super(ActivateNumberEndpoint, self).handle_response(response)
        except NumbersException as ex:
            raise NumberNotFoundException(message=ex.args[0], response=ex.http_response,
                                          is_from_server=ex.is_from_server)
        return self.process_response_model(response.body, ActiveNumber)


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

    def handle_response(self, response: HTTPResponse) -> list[AvailableNumber]:
        """
        Processes the API response and maps it to a response model.

        Args:
            response (HTTPResponse): The raw HTTP response object received from the API.

        Returns:
            list[AvailableNumber]: The response model containing the parsed response data.
        """
        super(AvailableNumbersEndpoint, self).handle_response(response)
        response = self.process_response_model(response.body, ListAvailableNumbersResponse)
        return response.available_numbers


class RentAnyNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to rent an available virtual number for a project.
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers:rentAny"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: RentAnyNumberRequest):
        super(RentAnyNumberEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data

    def request_body(self) -> str:
        request_data = self.request_data.model_dump(by_alias=True, exclude_none=True)
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> RentAnyNumberResponse:
        """
        Handles the response from the API call.

        Args:
            response (HTTPResponse): The response object from the API call.

        Returns:
            RentAnyNumberResponse: The response data mapped to the RentAnyNumberResponse model.
        """
        error = super(RentAnyNumberEndpoint, self).handle_response(response)
        if error:
            return error
        return self.process_response_model(response.body, RentAnyNumberResponse)


class SearchForNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to check the availability of a virtual number for a project.
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers/{phone_number}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: CheckNumberAvailabilityRequest):
        super(SearchForNumberEndpoint, self).__init__(project_id, request_data)

    def handle_response(self, response: HTTPResponse) -> CheckNumberAvailabilityResponse:
        """
        Processes the API response and maps it to a response

        Args:
            response (HTTPResponse): The raw HTTP response object received from the API.

        Returns:
            CheckNumberAvailabilityResponse: The response model containing the parsed response data
            of the requested phone number.
        """
        try:
            super(SearchForNumberEndpoint, self).handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(message=e.args[0], response=e.http_response, is_from_server=e.is_from_server)
        return self.process_response_model(response.body, CheckNumberAvailabilityResponse)
