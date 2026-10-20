from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.project_settings.internal.delete_project_settings_request import (
    DeleteProjectSettingsRequest,
)
from sinch.domains.conversation.models.v1.project_settings.internal.get_project_settings_request import (
    GetProjectSettingsRequest,
)
from sinch.domains.conversation.models.v1.project_settings.internal.project_settings_request import (
    ProjectSettingsRequest,
)
from sinch.domains.conversation.models.v1.project_settings.response.project_settings_response import (
    ProjectSettingsResponse,
)


class CreateProjectSettingsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/settings"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ProjectSettingsRequest,
        response_model=ProjectSettingsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetProjectSettingsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/settings"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: GetProjectSettingsRequest,
        response_model=ProjectSettingsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class UpdateProjectSettingsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/settings"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ProjectSettingsRequest,
        response_model=ProjectSettingsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DeleteProjectSettingsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/settings"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: DeleteProjectSettingsRequest,
    ):
        super().__init__(project_id, request_data)
