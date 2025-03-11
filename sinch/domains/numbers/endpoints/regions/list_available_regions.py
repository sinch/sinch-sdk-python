from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.numbers.models.regions import Region

from sinch.domains.numbers.models.regions.responses import ListAvailableRegionsResponse
from sinch.domains.numbers.models.regions.requests import ListAvailableRegionsForProjectRequest


class ListAvailableRegionsEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableRegions"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListAvailableRegionsForProjectRequest):
        super(ListAvailableRegionsEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id
        )

    def build_query_params(self) -> dict:
        query_params = {}
        if self.request_data.number_type:
            query_params["type"] = self.request_data.number_type

        if self.request_data.number_types:
            query_params["types"] = self.request_data.number_types

        return query_params

    def handle_response(self, response: HTTPResponse) -> ListAvailableRegionsResponse:
        super(ListAvailableRegionsEndpoint, self).handle_response(response)
        return ListAvailableRegionsResponse(
            [
                Region(
                    region_code=region["regionCode"],
                    region_name=region["regionName"],
                    types=region["types"]
                ) for region in response.body["availableRegions"]
            ]
        )
