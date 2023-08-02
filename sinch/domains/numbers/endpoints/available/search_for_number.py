from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.numbers.models.available.responses import CheckNumberAvailabilityResponse
from sinch.domains.numbers.models.available.requests import CheckNumberAvailabilityRequest

class SearchForNumberEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers/{phone_number}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: CheckNumberAvailabilityRequest):
        super(SearchForNumberEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id,
            phone_number=self.request_data.phone_number
        )

    def handle_response(self, response: HTTPResponse) -> CheckNumberAvailabilityResponse:
        super(SearchForNumberEndpoint, self).handle_response(response)
        return CheckNumberAvailabilityResponse(
            phone_number=response.body["phoneNumber"],
            region_code=response.body["regionCode"],
            type=response.body["type"],
            capability=response.body["capability"],
            setup_price=response.body["setupPrice"],
            monthly_price=response.body["monthlyPrice"],
            payment_interval_months=response.body["paymentIntervalMonths"],
            supporting_documentation_required=response.body["supportingDocumentationRequired"]
        )
