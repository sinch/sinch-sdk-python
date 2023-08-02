from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.numbers.models import Number

from sinch.domains.numbers.models.available.requests import ListAvailableNumbersRequest
from sinch.domains.numbers.models.available.responses import ListAvailableNumbersResponse

class AvailableNumbersEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListAvailableNumbersRequest):
        super(AvailableNumbersEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id
        )

    def build_query_params(self) -> dict:
        return {
            "regionCode": self.request_data.region_code,
            "type": self.request_data.number_type,
            "size": self.request_data.page_size,
            "capabilities": self.request_data.capabilities,
            "numberPattern.pattern": self.request_data.number_pattern,
            "numberPattern.searchPattern": self.request_data.number_search_pattern
        }

    def handle_response(self, response: HTTPResponse) -> ListAvailableNumbersResponse:
        super(AvailableNumbersEndpoint, self).handle_response(response)
        return ListAvailableNumbersResponse(
            [
                Number(
                    phone_number=number["phoneNumber"],
                    region_code=number["regionCode"],
                    type=number["type"],
                    capability=number["capability"],
                    setup_price=number["setupPrice"],
                    monthly_price=number["monthlyPrice"],
                    payment_interval_months=number["paymentIntervalMonths"],
                    supporting_documentation_required=number["supportingDocumentationRequired"]
                ) for number in response.body["availableNumbers"]
            ]
        )
