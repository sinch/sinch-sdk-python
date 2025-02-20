from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.numbers.models.active.list_active_numbers_request import ListActiveNumbersRequest
from sinch.domains.numbers.models.active.list_active_numbers_response import ListActiveNumbersResponse


class ListActiveNumbersEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/activeNumbers"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListActiveNumbersRequest):
        super(ListActiveNumbersEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        return self.request_data.model_dump(exclude_none=True, by_alias=True)

    def request_body(self) -> str:
        return ""

    def handle_response(self, response: HTTPResponse) -> ListActiveNumbersResponse:
        super(ListActiveNumbersEndpoint, self).handle_response(response)
        return self.process_response_model(response.body, ListActiveNumbersResponse)
