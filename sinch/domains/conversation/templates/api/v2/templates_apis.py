from typing import List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.conversation.api.v1.base.base_conversation import (
    BaseConversation,
)
from sinch.domains.conversation.templates.api.v2.internal.templates_endpoints import (
    CreateTemplateEndpoint,
    DeleteTemplateEndpoint,
    GetTemplateEndpoint,
    ListTemplatesEndpoint,
    ListTranslationsEndpoint,
    UpdateTemplateEndpoint,
)
from sinch.domains.conversation.templates.models.v2.internal.create_template_request import (
    CreateTemplateRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_templates_request import (
    ListTemplatesRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_templates_response import (
    ListTemplatesResponse,
)
from sinch.domains.conversation.templates.models.v2.internal.list_translations_request import (
    ListTranslationsRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_translations_response import (
    ListTranslationsResponse,
)
from sinch.domains.conversation.templates.models.v2.internal.template_id_request import (
    TemplateIdRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.update_template_request import (
    UpdateTemplateRequest,
)
from sinch.domains.conversation.templates.models.v2.response.template_response import (
    TemplateResponse,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslation,
)
from sinch.domains.conversation.templates.models.v2.types.template_translation_dict import (
    TemplateTranslationDict,
)


class Templates(BaseConversation):
    def create(
        self,
        default_translation: str,
        translations: List[TemplateTranslationDict],
        id: UnsetOr[Optional[str]] = UNSET,
        description: UnsetOr[Optional[str]] = UNSET,
        version: UnsetOr[Optional[int]] = UNSET,
        **kwargs,
    ) -> TemplateResponse:
        """
        Creates a new template under the given project ID.

        :param default_translation: The default translation to use if not specified. Specified as a BCP-47
            ``language_code`` and the ``language_code`` must exist in the translations list. (required)
        :type default_translation: str
        :param translations: The translations of the template. Each translation defines exactly one
            message type (``text_message``, ``card_message``, ``carousel_message``, ``choice_message``,
            ``location_message``, ``media_message``, ``template_message``, ``list_message`` or
            ``contact_info_message``). (required)
        :type translations: List[TemplateTranslationDict]
        :param id: The id of the template. If not specified, an ID is generated. Must be unique for a
            given project. (optional)
        :type id: UnsetOr[Optional[str]]
        :param description: The description of the template. (optional)
        :type description: UnsetOr[Optional[str]]
        :param version: The version of the template. If not specified, the server defaults it to 1.
            (optional)
        :type version: UnsetOr[Optional[int]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The created template.
        :rtype: TemplateResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = CreateTemplateRequest(
            default_translation=default_translation,
            translations=translations,
            **strip_unset(
                {"id": id, "description": description, "version": version}
            ),
            **kwargs,
        )
        return self._request(CreateTemplateEndpoint, request_data)

    def delete(self, template_id: str, **kwargs) -> None:
        """
        Deletes a template under the given project ID.

        :param template_id: The ID of the template to delete. (required)
        :type template_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = TemplateIdRequest(template_id=template_id, **kwargs)
        return self._request(DeleteTemplateEndpoint, request_data)

    def get(self, template_id: str, **kwargs) -> TemplateResponse:
        """
        Fetches a template under the given project ID.

        :param template_id: The ID of the template to fetch. (required)
        :type template_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The template details.
        :rtype: TemplateResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = TemplateIdRequest(template_id=template_id, **kwargs)
        return self._request(GetTemplateEndpoint, request_data)

    def list(
        self, **kwargs
    ) -> Paginator[ListTemplatesResponse, TemplateResponse]:
        """
        Lists all templates belonging to the given project ID.

        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: A paginator for iterating through the templates.
        :rtype: Paginator[ListTemplatesResponse, TemplateResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListTemplatesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListTemplatesRequest(**kwargs),
            ),
        )

    def list_translations(
        self,
        template_id: str,
        language_code: Optional[str] = None,
        translation_version: Optional[str] = None,
        **kwargs,
    ) -> Paginator[ListTranslationsResponse, TemplateTranslation]:
        """
        Lists all translations for a template under the given project ID.

        :param template_id: The ID of the template to fetch. (required)
        :type template_id: str
        :param language_code: The translation's language code. (optional)
        :type language_code: Optional[str]
        :param translation_version: The translation's version. (optional)
        :type translation_version: Optional[str]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: A paginator for iterating through the translations.
        :rtype: Paginator[ListTranslationsResponse, TemplateTranslation]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListTranslationsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListTranslationsRequest(
                    template_id=template_id,
                    language_code=language_code,
                    translation_version=translation_version,
                    **kwargs,
                ),
            ),
        )

    def update(
        self,
        template_id: str,
        version: int,
        default_translation: UnsetOr[Optional[str]] = UNSET,
        translations: UnsetOr[Optional[List[TemplateTranslationDict]]] = UNSET,
        description: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> TemplateResponse:
        """
        Updates a template under the given project ID.

        The template is replaced with the provided content; omitted parameters
        are not sent.

        :param template_id: The id of the template to be updated. Specified or automatically generated
            during template creation. Unique per project. (required)
        :type template_id: str
        :param version: The latest version of the template. It must match the current version of the
            template in order for the update to be successful. (required)
        :type version: int
        :param default_translation: The default translation to use if not specified. Specified as a
            BCP-47 ``language_code`` and the ``language_code`` must exist in the translations list.
            (optional)
        :type default_translation: UnsetOr[Optional[str]]
        :param translations: The translations of the template. Each translation defines exactly one
            message type. (optional)
        :type translations: UnsetOr[Optional[List[TemplateTranslationDict]]]
        :param description: The description of the template. (optional)
        :type description: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The updated template.
        :rtype: TemplateResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = UpdateTemplateRequest(
            template_id=template_id,
            version=version,
            **strip_unset(
                {
                    "default_translation": default_translation,
                    "translations": translations,
                    "description": description,
                }
            ),
            **kwargs,
        )
        return self._request(UpdateTemplateEndpoint, request_data)
