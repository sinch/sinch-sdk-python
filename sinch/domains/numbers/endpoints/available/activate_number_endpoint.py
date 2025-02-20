from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.domains.numbers.exceptions import NumberNotFoundException, NumbersException
from sinch.domains.numbers.models.available import ActivateNumberRequest, ActivateNumberResponse


class ActivateNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to activate a virtual number for a project.
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers/{phone_number}:rent"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ActivateNumberRequest):
        super(ActivateNumberEndpoint, self).__init__(project_id, request_data)

    def handle_response(self, response: HTTPResponse) -> ActivateNumberResponse:
        try:
            super(ActivateNumberEndpoint, self).handle_response(response)
        except NumbersException as ex:
            raise NumberNotFoundException(message=ex.args[0], response=ex.http_response,
                                          is_from_server=ex.is_from_server)
        return self.process_response_model(response.body, ActivateNumberResponse)
