from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.sms.models.groups.requests import ListSMSGroupRequest
from sinch.domains.sms.models.groups.responses import SinchListSMSGroupResponse
from sinch.domains.sms.models.groups import SMSGroup


class ListSMSGroupEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_or_service_id}/groups"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, request_data: ListSMSGroupRequest, sinch):
        super().__init__(request_data, sinch)

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin, project_or_service_id=self.project_or_service_id
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
                    auto_update=response.body.get("auto_update"),
                )
                for group in response.body["groups"]
            ],
            page=response.body.get("page"),
            page_size=response.body.get("page_size"),
            count=response.body.get("count"),
        )
