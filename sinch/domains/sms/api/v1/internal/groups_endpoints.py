import json

from pydantic import StrictStr, TypeAdapter, conlist

from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal.base.sms_endpoint import SmsEndpoint
from sinch.domains.sms.models.v1.internal.group_id_request import (
    GroupIdRequest,
)
from sinch.domains.sms.models.v1.internal.group_request import GroupRequest
from sinch.domains.sms.models.v1.internal.list_groups_request import (
    ListGroupsRequest,
)
from sinch.domains.sms.models.v1.internal.replace_group_request import (
    ReplaceGroupRequest,
)
from sinch.domains.sms.models.v1.internal.update_group_request import (
    UpdateGroupRequest,
)
from sinch.domains.sms.models.v1.response.group_response import GroupResponse
from sinch.domains.sms.models.v1.response.list_group_members_response import (
    ListGroupMembersResponse,
)
from sinch.domains.sms.models.v1.response.list_groups_response import (
    ListGroupsResponse,
)


class CreateGroupEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: GroupRequest,
        response_model=GroupResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ListGroupsEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS: set = {"page", "page_size"}

    def __init__(
        self,
        project_id: str,
        request_data: ListGroupsRequest,
        response_model=ListGroupsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetGroupEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups/{group_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: GroupIdRequest,
        response_model=GroupResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ReplaceGroupEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups/{group_id}"
    HTTP_METHOD = HTTPMethods.PUT.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ReplaceGroupRequest,
        response_model=GroupResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class UpdateGroupEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups/{group_id}"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: UpdateGroupRequest,
        response_model=GroupResponse,
    ):
        super().__init__(project_id, request_data, response_model)

    def request_body(self):
        """None fields are sent as explicit null, not omitted, so the API can clear a field."""
        path_params = self._get_path_params_from_url()
        request_data = self.request_data.model_dump(
            mode="json",
            by_alias=True,
            exclude=path_params,
        )
        return json.dumps(request_data)


class DeleteGroupEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups/{group_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: GroupIdRequest):
        super().__init__(project_id, request_data)


class ListGroupMembersEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/groups/{group_id}/members"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: GroupIdRequest):
        super().__init__(project_id, request_data)

    def handle_response(
        self, response: HTTPResponse
    ) -> ListGroupMembersResponse:
        """The API returns a bare JSON array of members, not a {"members": [...]} object."""
        self._raise_for_error(response)
        members = TypeAdapter(conlist(StrictStr)).validate_python(
            response.body
        )
        return ListGroupMembersResponse(members=members)
