from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.internal.utils import query_params_to_comma_joined_lists
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.apps.internal.app_id_request import (
    AppIdRequest,
)
from sinch.domains.conversation.models.v1.apps.internal.list_apps_request import (
    ListAppsRequest,
)
from sinch.domains.conversation.models.v1.apps.internal.list_apps_response import (
    ListAppsResponse,
)
from sinch.domains.conversation.models.v1.apps.request.create_app_request import (
    CreateAppRequest,
)
from sinch.domains.conversation.models.v1.apps.request.update_app_request import (
    UpdateAppRequest,
)
from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)


class ListAppsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ListAppsRequest,
        response_model=ListAppsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class CreateAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: CreateAppRequest,
        response_model=AppResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DeleteAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: AppIdRequest):
        super().__init__(project_id, request_data)


class GetAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: AppIdRequest,
        response_model=AppResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class UpdateAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS_EXPLODE_FALSE = {"update_mask"}

    def __init__(
        self,
        project_id: str,
        request_data: UpdateAppRequest,
        response_model=AppResponse,
    ):
        super().__init__(project_id, request_data, response_model)

    def build_query_params(self) -> dict:
        """update_mask lists which fields were set, it isn't a request_data field itself."""
        body_data = self._build_body_data()
        if not body_data:
            return {}
        return query_params_to_comma_joined_lists(
            {"update_mask": list(body_data.keys())}, ["update_mask"]
        )
