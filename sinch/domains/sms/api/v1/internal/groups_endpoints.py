


import json

from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.utils import model_dump_for_query_params
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.api.v1.internal.base.sms_endpoint import SmsEndpoint
from sinch.domains.sms.models.v1.internal.group_request import GroupRequest
from sinch.domains.sms.models.v1.internal.list_groups_request import (
    ListGroupsRequest,
)
from sinch.domains.sms.models.v1.response.list_groups_response import (
    ListGroupsResponse,
)
from sinch.domains.sms.models.v1.response.group_response import GroupResponse


class CreateGroupEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value


    def __init__(self, project_id: str, request_data: GroupRequest):
        super(CreateGroupEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        # Use mode='json' to serialize datetime objects to ISO-8601 strings
        request_data = self.request_data.model_dump(
            mode="json", by_alias=True, exclude_none=True
        )
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> GroupResponse:
        try:
            super(CreateGroupEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, GroupResponse)
    
class ListGroupsEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListGroupsRequest):
        super(ListGroupsEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        return model_dump_for_query_params(self.request_data)

    def handle_response(
        self, response: HTTPResponse
    ) -> ListGroupsResponse:
        try:
            super(ListGroupsEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(
            response.body, ListGroupsResponse
        )