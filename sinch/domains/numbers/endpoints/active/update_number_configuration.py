from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.internal.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.numbers.models.active.requests import UpdateNumberConfigurationRequest
from sinch.domains.numbers.models.active.responses import UpdateNumberConfigurationResponse


class UpdateNumberConfigurationEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/activeNumbers/{phone_number}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: UpdateNumberConfigurationRequest):
        super(UpdateNumberConfigurationEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id,
            phone_number=self.request_data.phone_number
        )

    def request_body(self):
        self.request_data.phone_number = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> UpdateNumberConfigurationResponse:
        super(UpdateNumberConfigurationEndpoint, self).handle_response(response)
        return UpdateNumberConfigurationResponse(
            phone_number=response.body["phoneNumber"],
            project_id=response.body["projectId"],
            display_name=response.body["displayName"],
            region_code=response.body["regionCode"],
            type=response.body["type"],
            capability=response.body["capability"],
            money=response.body["money"],
            payment_interval_months=response.body["paymentIntervalMonths"],
            next_charge_date=response.body["nextChargeDate"],
            expire_at=response.body["expireAt"],
            sms_configuration=response.body["smsConfiguration"],
            voice_configuration=response.body["voiceConfiguration"]
        )
