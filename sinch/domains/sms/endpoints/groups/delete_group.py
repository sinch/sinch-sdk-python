from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.sms.models.groups.requests import DeleteSMSGroupRequest
from sinch.domains.sms.models.groups.responses import SinchDeleteSMSGroupResponse


class DeleteSMSGroupEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups/{group_id}"
    HTTP_METHOD = HTTPMethod.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: DeleteSMSGroupRequest):
        super(DeleteSMSGroupEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id,
            group_id=self.request_data.group_id
        )

    def handle_response(self, response: HTTPResponse):
        super(DeleteSMSGroupEndpoint, self).handle_response(response)
        return SinchDeleteSMSGroupResponse()
