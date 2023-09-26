from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.numbers.models.active import ActiveNumber
from sinch.domains.numbers.models.active.requests import ListActiveNumbersRequest
from sinch.domains.numbers.models.active.responses import ListActiveNumbersResponse


class ListActiveNumbersEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/activeNumbers"
    HTTP_METHOD = HTTPMethod.GET
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: ListActiveNumbersRequest):
        super(ListActiveNumbersEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id
        )

    def build_query_params(self) -> dict:
        params = {
            "regionCode": self.request_data.region_code,
            "type": self.request_data.number_type,
        }

        if self.request_data.capabilities:
            params["capabilities"] = self.request_data.capabilities

        if self.request_data.number_pattern:
            params["numberPattern.pattern"] = self.request_data.number_pattern

        if self.request_data.number_search_pattern:
            params["numberPattern.searchPattern"] = self.request_data.capabilities

        if self.request_data.page_size:
            params["pageSize"] = self.request_data.page_size

        if self.request_data.page_token:
            params["pageToken"] = self.request_data.page_token

        return params

    def handle_response(self, response: HTTPResponse) -> ListActiveNumbersResponse:
        super(ListActiveNumbersEndpoint, self).handle_response(response)
        return ListActiveNumbersResponse(
            [
                ActiveNumber(
                    phone_number=number["phoneNumber"],
                    project_id=number["projectId"],
                    display_name=number["displayName"],
                    region_code=number["regionCode"],
                    type=number["type"],
                    capability=number["capability"],
                    money=number["money"],
                    payment_interval_months=number["paymentIntervalMonths"],
                    next_charge_date=number["nextChargeDate"],
                    expire_at=number["expireAt"],
                    sms_configuration=number["smsConfiguration"],
                    voice_configuration=number["voiceConfiguration"]
                ) for number in response.body["activeNumbers"]
            ],
            next_page_token=response.body["nextPageToken"]
        )
