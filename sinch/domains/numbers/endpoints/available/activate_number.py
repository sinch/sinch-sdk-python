from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.numbers.models.available.requests import ActivateNumberRequest
from sinch.domains.numbers.models.available.responses import ActivateNumberResponse


class ActivateNumberEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers/{phone_number}:rent"
    HTTP_METHOD = HTTPMethod.POST
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: ActivateNumberRequest):
        super(ActivateNumberEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id,
            phone_number=self.request_data.phone_number
        )

    def handle_response(self, response: HTTPResponse) -> ActivateNumberResponse:
        super(ActivateNumberEndpoint, self).handle_response(response)
        return ActivateNumberResponse(
            phone_number=response.body["phoneNumber"],
            region_code=response.body["regionCode"],
            type=response.body["type"],
            capability=response.body["capability"]
        )
