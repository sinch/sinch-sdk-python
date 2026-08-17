from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.exceptions import (
    NumberNotFoundException,
    NumbersException,
)
from sinch.domains.numbers.api.v1.internal.base import NumbersEndpoint
from sinch.domains.numbers.models.v1.internal import (
    ListAvailableNumbersRequest,
    ListAvailableNumbersResponse,
    NumberRequest,
    RentAnyNumberRequest,
    RentNumberRequest,
)
from sinch.domains.numbers.models.v1.response import (
    ActiveNumber,
    AvailableNumber,
)


class RentNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to rent a virtual number for a project.
    """

    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers/{phone_number}:rent"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: RentNumberRequest,
        response_model=ActiveNumber,
    ):
        super().__init__(project_id, request_data, response_model)

    def handle_response(self, response: HTTPResponse) -> ActiveNumber:
        try:
            super().handle_response(response)
        except NumbersException as ex:
            raise NumberNotFoundException(
                message=ex.args[0],
                response=ex.http_response,
                is_from_server=ex.is_from_server,
            )
        return self._process_response_model(response.body, ActiveNumber)


class AvailableNumbersEndpoint(NumbersEndpoint):
    """
    Endpoint to list available virtual numbers for a project.
    """

    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS: set = {
        "region_code",
        "number_type",
        "capabilities",
        "number_search_pattern",
        "number_pattern",
        "page_size",
    }

    def __init__(
        self,
        project_id: str,
        request_data: ListAvailableNumbersRequest,
        response_model=ListAvailableNumbersResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class RentAnyNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to rent an available virtual number for a project.
    """

    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers:rentAny"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: RentAnyNumberRequest,
        response_model=ActiveNumber,
    ):
        super().__init__(project_id, request_data, response_model)


class SearchForNumberEndpoint(NumbersEndpoint):
    """
    Endpoint to check the availability of a virtual number for a project.
    """

    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/availableNumbers/{phone_number}"
    )
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: NumberRequest,
        response_model=AvailableNumber,
    ):
        super().__init__(project_id, request_data, response_model)

    def handle_response(self, response: HTTPResponse) -> AvailableNumber:
        try:
            super().handle_response(response)
        except NumbersException as e:
            raise NumberNotFoundException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self._process_response_model(response.body, AvailableNumber)
