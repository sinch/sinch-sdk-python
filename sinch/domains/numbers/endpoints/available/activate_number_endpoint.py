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
        self.request_data = request_data

    def handle_response(self, response: HTTPResponse) -> ActivateNumberResponse:
        error = super(ActivateNumberEndpoint, self).handle_response(response)
        if error:
            return error
        return self.process_response_model(response.body, ActivateNumberResponse)
