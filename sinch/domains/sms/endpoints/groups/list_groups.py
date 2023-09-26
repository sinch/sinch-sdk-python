from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.sms.models.groups.requests import ListSMSGroupRequest
from sinch.domains.sms.models.groups.responses import SinchListSMSGroupResponse
from sinch.domains.sms.models.groups import SMSGroup


class ListSMSGroupEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups"
    HTTP_METHOD = HTTPMethod.GET
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: ListSMSGroupRequest):
        super(ListSMSGroupEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id
        )

    def build_query_params(self):
        return self.request_data.as_dict()

    def handle_response(self, response: HTTPResponse):
        super(ListSMSGroupEndpoint, self).handle_response(response)
        return SinchListSMSGroupResponse(
            groups=[
                SMSGroup(
                    id=group.get("id"),
                    size=group.get("size"),
                    created_at=group.get("created_at"),
                    modified_at=group.get("modified_at"),
                    name=group.get("name"),
                    child_groups=group.get("child_groups"),
                    auto_update=response.body.get("auto_update")
                ) for group in response.body["groups"]
            ],
            page=response.body.get("page"),
            page_size=response.body.get("page_size"),
            count=response.body.get("count")
        )
