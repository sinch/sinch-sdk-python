import json
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.numbers.models.available.requests import RentAnyNumberRequest
from sinch.domains.numbers.models.available.responses import RentAnyNumberResponse


class RentAnyNumberEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/availableNumbers:rentAny"
    HTTP_METHOD = HTTPMethod.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: RentAnyNumberRequest):
        super(RentAnyNumberEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id
        )

    def request_body(self):
        request_data = self.request_data.as_dict()
        request_body = {}

        if request_data.get("region_code"):
            request_body["regionCode"] = request_data["region_code"]

        if request_data.get("type_"):
            request_body["type"] = request_data["type_"]

        if request_data.get("number_pattern"):
            request_body["numberPattern"] = request_data["number_pattern"]

        if request_data.get("capabilities"):
            request_body["capabilities"] = request_data["capabilities"]

        if request_data.get("sms_configuration"):
            request_body["smsConfiguration"] = request_data["sms_configuration"]

        if request_data.get("voice_configuration"):
            request_body["voiceConfiguration"] = request_data["voice_configuration"]

        if request_data.get("callback_url"):
            request_body["callbackUrl"] = request_data["callback_url"]

        return json.dumps(request_body)

    def handle_response(self, response: HTTPResponse) -> RentAnyNumberResponse:
        super(RentAnyNumberEndpoint, self).handle_response(response)
        return RentAnyNumberResponse(
            phone_number=response.body["phoneNumber"],
            region_code=response.body["regionCode"],
            type=response.body["type"],
            capability=response.body["capability"],
            project_id=response.body["projectId"],
            callback_url=response.body["callbackUrl"],
            expire_at=response.body["expireAt"],
            money=response.body["money"],
            next_charge_date=response.body["nextChargeDate"],
            sms_configuration=response.body["smsConfiguration"],
            voice_configuration=response.body["voiceConfiguration"],
            payment_interval_months=response.body["paymentIntervalMonths"]
        )
