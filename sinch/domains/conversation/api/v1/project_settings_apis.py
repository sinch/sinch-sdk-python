from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.conversation.api.v1.base import BaseConversation
from sinch.domains.conversation.api.v1.internal.project_settings_endpoints import (
    CreateProjectSettingsEndpoint,
    DeleteProjectSettingsEndpoint,
    GetProjectSettingsEndpoint,
    UpdateProjectSettingsEndpoint,
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
from sinch.domains.conversation.models.v1.project_settings.types.contact_settings_dict import (
    ContactSettingsDict,
)


class ProjectSettings(BaseConversation):
    def create(
        self,
        contact_settings: UnsetOr[ContactSettingsDict] = UNSET,
        **kwargs,
    ) -> ProjectSettingsResponse:
        """
        Creates initial settings for the project. Useful for enabling features like Unified
        Contact ID. For new projects with no existing contacts, you can enable Unified Contact ID
        immediately.

        :param contact_settings: (optional) Settings related to contact management for the project.
        :type contact_settings: UnsetOr[ContactSettingsDict]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The created project settings.
        :rtype: ProjectSettingsResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = ProjectSettingsRequest(
            **strip_unset({"contact_settings": contact_settings}),
            **kwargs,
        )
        return self._request(CreateProjectSettingsEndpoint, request_data)

    def get(self, **kwargs) -> ProjectSettingsResponse:
        """
        Retrieves the current settings for the project, including contact management options such
        as Unified Contact ID.

        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The current project settings.
        :rtype: ProjectSettingsResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = GetProjectSettingsRequest(**kwargs)
        return self._request(GetProjectSettingsEndpoint, request_data)

    def update(
        self,
        contact_settings: UnsetOr[ContactSettingsDict] = UNSET,
        **kwargs,
    ) -> ProjectSettingsResponse:
        """
        Updates project settings (e.g. enabling/disabling Unified Contact ID). For existing
        projects, you must resolve all identity conflicts before enabling Unified Contact ID.

        :param contact_settings: (optional) Settings related to contact management for the project.
        :type contact_settings: UnsetOr[ContactSettingsDict]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The updated project settings.
        :rtype: ProjectSettingsResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = ProjectSettingsRequest(
            **strip_unset({"contact_settings": contact_settings}),
            **kwargs,
        )
        return self._request(UpdateProjectSettingsEndpoint, request_data)

    def delete(self, **kwargs) -> None:
        """
        Deletes all project-level settings for the project.

        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = DeleteProjectSettingsRequest(**kwargs)
        return self._request(DeleteProjectSettingsEndpoint, request_data)
