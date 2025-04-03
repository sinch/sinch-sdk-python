import json
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.exceptions import NumbersException, NumberNotFoundException
from sinch.domains.numbers.api.v1.internal.base import NumbersEndpoint
from sinch.domains.numbers.models.v1.internal import (
    ListActiveNumbersRequest, ListActiveNumbersResponse, NumberRequest, UpdateNumberConfigurationRequest
)
from sinch.domains.numbers.models.v1.response import ActiveNumber


class GetNumberConfigurationEndpoint(NumbersEndpoint):
    """
    Endpoint to get the configuration of a specific number
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/activeNumbers/{phone_number}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: NumberRequest):
        super(GetNumberConfigurationEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(self, response: HTTPResponse) -> ActiveNumber:
        try:
            super(GetNumberConfigurationEndpoint, self).handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(message=e.args[0], response=e.http_response, is_from_server=e.is_from_server)
        return self.process_response_model(response.body, ActiveNumber)


class ListActiveNumbersEndpoint(NumbersEndpoint):
    """
    Endpoint to list all active numbers for a project.
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/activeNumbers"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListActiveNumbersRequest):
        super(ListActiveNumbersEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        return self.request_data.model_dump(exclude_none=True, by_alias=True)

    def handle_response(self, response: HTTPResponse) -> ListActiveNumbersResponse:
        super(ListActiveNumbersEndpoint, self).handle_response(response)
        return self.process_response_model(response.body, ListActiveNumbersResponse)


class ReleaseNumberFromProjectEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/activeNumbers/{phone_number}:release"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id, request_data: NumberRequest):
        super(ReleaseNumberFromProjectEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(self, response: HTTPResponse) -> ActiveNumber:
        try:
            super(ReleaseNumberFromProjectEndpoint, self).handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(message=e.args[0], response=e.http_response, is_from_server=e.is_from_server)
        return self.process_response_model(response.body, ActiveNumber)


class UpdateNumberConfigurationEndpoint(NumbersEndpoint):
    """
    Endpoint to update the configuration of a specific number
    """
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/activeNumbers/{phone_number}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: UpdateNumberConfigurationRequest):
        super(UpdateNumberConfigurationEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        request_data = self.request_data.model_dump(by_alias=True, exclude_none=True)
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> ActiveNumber:
        try:
            super(UpdateNumberConfigurationEndpoint, self).handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(message=e.args[0], response=e.http_response, is_from_server=e.is_from_server)
        return self.process_response_model(response.body, ActiveNumber)
