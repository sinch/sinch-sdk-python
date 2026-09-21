from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.exceptions import (
    NumberNotFoundException,
    NumbersException,
)
from sinch.domains.numbers.api.v1.internal.base import NumbersEndpoint
from sinch.domains.numbers.models.v1.internal import (
    ListActiveNumbersRequest,
    ListActiveNumbersResponse,
    NumberRequest,
    UpdateNumberConfigurationRequest,
)
from sinch.domains.numbers.models.v1.response import ActiveNumber


class GetNumberConfigurationEndpoint(NumbersEndpoint):
    """
    Endpoint to get the configuration of a specific number
    """

    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/activeNumbers/{phone_number}"
    )
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: NumberRequest,
        response_model=ActiveNumber,
    ):
        super().__init__(project_id, request_data, response_model)

    def handle_response(self, response: HTTPResponse) -> ActiveNumber:
        try:
            super().handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self._process_response_model(response.body, ActiveNumber)


class ListActiveNumbersEndpoint(NumbersEndpoint):
    """
    Endpoint to list all active numbers for a project.
    """

    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/activeNumbers"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS: set = {
        "region_code",
        "number_type",
        "page_size",
        "capabilities",
        "number_search_pattern",
        "number_pattern",
        "page_token",
        "order_by",
    }

    def __init__(
        self,
        project_id: str,
        request_data: ListActiveNumbersRequest,
        response_model=ListActiveNumbersResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ReleaseNumberFromProjectEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/activeNumbers/{phone_number}:release"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id,
        request_data: NumberRequest,
        response_model=ActiveNumber,
    ):
        super(ReleaseNumberFromProjectEndpoint, self).__init__(
            project_id, request_data, response_model
        )

    def handle_response(self, response: HTTPResponse) -> ActiveNumber:
        try:
            super().handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self._process_response_model(response.body, ActiveNumber)


class UpdateNumberConfigurationEndpoint(NumbersEndpoint):
    """
    Endpoint to update the configuration of a specific number
    """

    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/activeNumbers/{phone_number}"
    )
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: UpdateNumberConfigurationRequest,
        response_model=ActiveNumber,
    ):
        super().__init__(project_id, request_data, response_model)

    def handle_response(self, response: HTTPResponse) -> ActiveNumber:
        try:
            super().handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self._process_response_model(response.body, ActiveNumber)
