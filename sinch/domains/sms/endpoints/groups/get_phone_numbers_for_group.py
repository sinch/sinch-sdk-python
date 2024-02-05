from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.sms.models.groups.requests import GetSMSGroupPhoneNumbersRequest
from sinch.domains.sms.models.groups.responses import SinchGetSMSGroupPhoneNumbersResponse


class GetSMSGroupPhoneNumbersEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups/{group_id}/members"
    HTTP_METHOD = HTTPMethod.GET
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: GetSMSGroupPhoneNumbersRequest):
        super(GetSMSGroupPhoneNumbersEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id,
            group_id=self.request_data.group_id
        )

    def handle_response(self, response: HTTPResponse):
        super(GetSMSGroupPhoneNumbersEndpoint, self).handle_response(response)
        return SinchGetSMSGroupPhoneNumbersResponse(
            phone_numbers=response.body
        )
