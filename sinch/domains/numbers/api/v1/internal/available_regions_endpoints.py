from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.exceptions import (
    NumberNotFoundException,
    NumbersException,
)
from sinch.domains.numbers.api.v1.internal.base.numbers_endpoint import (
    NumbersEndpoint,
)
from sinch.domains.numbers.models.v1.internal import (
    ListAvailableRegionsRequest,
    ListAvailableRegionsResponse,
)


class ListAvailableRegionsEndpoint(NumbersEndpoint):
    """
    Endpoint to list all the regions that have numbers assigned to a project
    """

    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableRegions"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS: set = {"types"}

    def __init__(
        self,
        project_id: str,
        request_data: ListAvailableRegionsRequest,
        response_model=ListAvailableRegionsResponse,
    ):
        super().__init__(project_id, request_data, response_model)

    def handle_response(
        self, response: HTTPResponse
    ) -> ListAvailableRegionsResponse:
        try:
            super(ListAvailableRegionsEndpoint, self).handle_response(response)
        except NumbersException as ex:
            raise NumberNotFoundException(
                message=ex.args[0],
                response=ex.http_response,
                is_from_server=ex.is_from_server,
            )
        return self._process_response_model(
            response.body, ListAvailableRegionsResponse
        )
