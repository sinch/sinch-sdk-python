from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.sms.models.groups.requests import UpdateSMSGroupRequest
from sinch.domains.sms.models.groups.responses import UpdateSMSGroupResponse


class UpdateSMSGroupEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups/{group_id}"
    HTTP_METHOD = HTTPMethod.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: UpdateSMSGroupRequest):
        super(UpdateSMSGroupEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id,
            group_id=self.request_data.group_id
        )

    def request_body(self):
        self.request_data.group_id = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse):
        super(UpdateSMSGroupEndpoint, self).handle_response(response)
        return UpdateSMSGroupResponse(
            id=response.body.get("id"),
            size=response.body.get("size"),
            created_at=response.body.get("created_at"),
            modified_at=response.body.get("modified_at"),
            name=response.body.get("name"),
            child_groups=response.body.get("child_groups"),
            auto_update=response.body.get("auto_update")
        )
