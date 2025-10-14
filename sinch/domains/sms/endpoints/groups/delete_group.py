from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.sms.models.groups.requests import DeleteSMSGroupRequest
from sinch.domains.sms.models.groups.responses import SinchDeleteSMSGroupResponse


class DeleteSMSGroupEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_or_service_id}/groups/{group_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, request_data: DeleteSMSGroupRequest, sinch):
        super().__init__(request_data, sinch)

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_or_service_id=self.project_or_service_id,
            group_id=self.request_data.group_id,
        )

    def handle_response(self, response: HTTPResponse):
        super(DeleteSMSGroupEndpoint, self).handle_response(response)
        return SinchDeleteSMSGroupResponse()
