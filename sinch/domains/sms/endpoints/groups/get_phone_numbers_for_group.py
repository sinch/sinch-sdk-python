from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.sms.models.groups.requests import GetSMSGroupPhoneNumbersRequest
from sinch.domains.sms.models.groups.responses import SinchGetSMSGroupPhoneNumbersResponse


class GetSMSGroupPhoneNumbersEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_or_service_id}/groups/{group_id}/members"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, request_data: GetSMSGroupPhoneNumbersRequest, sinch):
        super().__init__(request_data, sinch)

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_or_service_id=self.project_or_service_id,
            group_id=self.request_data.group_id
        )

    def handle_response(self, response: HTTPResponse):
        super(GetSMSGroupPhoneNumbersEndpoint, self).handle_response(response)
        return SinchGetSMSGroupPhoneNumbersResponse(
            phone_numbers=response.body
        )
