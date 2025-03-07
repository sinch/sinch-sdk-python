import json
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.models.numbers import ActiveNumber
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.domains.numbers.exceptions import NumberNotFoundException, NumbersException
from sinch.domains.numbers.models.available import ActivateNumberRequest


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
