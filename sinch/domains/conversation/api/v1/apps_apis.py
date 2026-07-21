from typing import Literal, Optional, Union, overload

from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.domains.conversation.api.v1.base import BaseConversation
from sinch.domains.conversation.api.v1.internal.apps_endpoints import (
    CreateAppEndpoint,
    DeleteAppEndpoint,
    GetAppEndpoint,
    ListAppsEndpoint,
    UpdateAppEndpoint,
)
from sinch.domains.conversation.models.v1.apps.internal.app_id_request import (
    AppIdRequest,
)
from sinch.domains.conversation.models.v1.apps.internal.list_apps_custom_response import (
    ListAppsCustomResponse,
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
from sinch.domains.conversation.models.v1.apps.response.app_custom_response import (
    AppCustomResponse,
)
from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)
from sinch.domains.conversation.models.v1.apps.types import (
    ConversationMetadataReportViewType,
    DeliveryReportBasedFallbackDict,
    DispatchRetentionPolicyDict,
    EventDestinationSettingsDict,
    MessageRetrySettingsDict,
    RetentionPolicyDict,
    SmartConversationDict,
)
from sinch.domains.conversation.models.v1.credentials.types import (
    ConversationChannelCredentialsDict,
)
from sinch.domains.conversation.models.v1.types import (
    ProcessingModeType,
)


class Apps(BaseConversation):
    @overload
    def create(
        self,
        channel_credentials: ConversationChannelCredentialsDict,
        display_name: str,
        conversation_metadata_report_view: Optional[
            ConversationMetadataReportViewType
        ] = None,
        retention_policy: Optional[RetentionPolicyDict] = None,
        dispatch_retention_policy: Optional[
            DispatchRetentionPolicyDict
        ] = None,
        processing_mode: Optional[ProcessingModeType] = None,
        smart_conversation: Optional[SmartConversationDict] = None,
        event_destination_settings: Optional[
            EventDestinationSettingsDict
        ] = None,
        message_retry_settings: Optional[MessageRetrySettingsDict] = None,
        delivery_report_based_fallback: Optional[
            DeliveryReportBasedFallbackDict
        ] = None,
        *,
        raw_response: Literal[False] = False,
        **kwargs,
    ) -> AppCustomResponse: ...

    @overload
    def create(
        self,
        channel_credentials: ConversationChannelCredentialsDict,
        display_name: str,
        conversation_metadata_report_view: Optional[
            ConversationMetadataReportViewType
        ] = None,
        retention_policy: Optional[RetentionPolicyDict] = None,
        dispatch_retention_policy: Optional[
            DispatchRetentionPolicyDict
        ] = None,
        processing_mode: Optional[ProcessingModeType] = None,
        smart_conversation: Optional[SmartConversationDict] = None,
        event_destination_settings: Optional[
            EventDestinationSettingsDict
        ] = None,
        message_retry_settings: Optional[MessageRetrySettingsDict] = None,
        delivery_report_based_fallback: Optional[
            DeliveryReportBasedFallbackDict
        ] = None,
        *,
        raw_response: Literal[True],
        **kwargs,
    ) -> AppResponse: ...

    def create(
        self,
        channel_credentials: ConversationChannelCredentialsDict,
        display_name: str,
        conversation_metadata_report_view: Optional[
            ConversationMetadataReportViewType
        ] = None,
        retention_policy: Optional[RetentionPolicyDict] = None,
        dispatch_retention_policy: Optional[
            DispatchRetentionPolicyDict
        ] = None,
        processing_mode: Optional[ProcessingModeType] = None,
        smart_conversation: Optional[SmartConversationDict] = None,
        event_destination_settings: Optional[
            EventDestinationSettingsDict
        ] = None,
        message_retry_settings: Optional[MessageRetrySettingsDict] = None,
        delivery_report_based_fallback: Optional[
            DeliveryReportBasedFallbackDict
        ] = None,
        *,
        raw_response: bool = False,
        **kwargs,
    ) -> Union[AppResponse, AppCustomResponse]:
        """
        Creates a new Conversation API app for one or more channels. The app ID is
        generated at creation and returned in the response.

        :param channel_credentials: Channel credentials, keyed by channel. The order of the
            entries defines the app channel priority.
        :type channel_credentials: ConversationChannelCredentialsDict
        :param display_name: The display name for the app.
        :type display_name: str
        :param conversation_metadata_report_view: Whether conversation metadata is included in reports.
        :type conversation_metadata_report_view: Optional[ConversationMetadataReportViewType]
        :param retention_policy: The retention policy for messages and conversations.
        :type retention_policy: Optional[RetentionPolicyDict]
        :param dispatch_retention_policy: The retention policy for messages in dispatch mode.
        :type dispatch_retention_policy: Optional[DispatchRetentionPolicyDict]
        :param processing_mode: The processing mode for the app.
        :type processing_mode: Optional[ProcessingModeType]
        :param smart_conversation: Smart Conversation settings for the app.
        :type smart_conversation: Optional[SmartConversationDict]
        :param event_destination_settings: Settings for the destination of Sinch events.
        :type event_destination_settings: Optional[EventDestinationSettingsDict]
        :param message_retry_settings: Settings controlling message retry behavior.
        :type message_retry_settings: Optional[MessageRetrySettingsDict]
        :param delivery_report_based_fallback: Delivery-report-based channel fallback settings.
        :type delivery_report_based_fallback: Optional[DeliveryReportBasedFallbackDict]
        :param raw_response: When ``False`` (default) the response exposes ``channel_credentials``
            as a channel-keyed model. Set to ``True`` to get the raw ``AppResponse`` with
            ``channel_credentials`` as the server array.
        :type raw_response: bool
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The created app.
        :rtype: Union[AppResponse, AppCustomResponse]
        """
        request_data = CreateAppRequest(
            channel_credentials=channel_credentials,
            conversation_metadata_report_view=conversation_metadata_report_view,
            display_name=display_name,
            retention_policy=retention_policy,
            dispatch_retention_policy=dispatch_retention_policy,
            processing_mode=processing_mode,
            smart_conversation=smart_conversation,
            event_destination_settings=event_destination_settings,
            message_retry_settings=message_retry_settings,
            delivery_report_based_fallback=delivery_report_based_fallback,
            **kwargs,
        )
        response = self._request(
            CreateAppEndpoint,
            request_data,
            response_model=AppResponse if raw_response else AppCustomResponse,
        )
        return response

    @overload
    def update(
        self,
        app_id: str,
        channel_credentials: Optional[
            ConversationChannelCredentialsDict
        ] = None,
        display_name: Optional[str] = None,
        conversation_metadata_report_view: Optional[
            ConversationMetadataReportViewType
        ] = None,
        retention_policy: Optional[RetentionPolicyDict] = None,
        dispatch_retention_policy: Optional[
            DispatchRetentionPolicyDict
        ] = None,
        processing_mode: Optional[ProcessingModeType] = None,
        smart_conversation: Optional[SmartConversationDict] = None,
        event_destination_settings: Optional[
            EventDestinationSettingsDict
        ] = None,
        message_retry_settings: Optional[MessageRetrySettingsDict] = None,
        delivery_report_based_fallback: Optional[
            DeliveryReportBasedFallbackDict
        ] = None,
        *,
        raw_response: Literal[False] = False,
        **kwargs,
    ) -> AppCustomResponse: ...

    @overload
    def update(
        self,
        app_id: str,
        channel_credentials: Optional[
            ConversationChannelCredentialsDict
        ] = None,
        display_name: Optional[str] = None,
        conversation_metadata_report_view: Optional[
            ConversationMetadataReportViewType
        ] = None,
        retention_policy: Optional[RetentionPolicyDict] = None,
        dispatch_retention_policy: Optional[
            DispatchRetentionPolicyDict
        ] = None,
        processing_mode: Optional[ProcessingModeType] = None,
        smart_conversation: Optional[SmartConversationDict] = None,
        event_destination_settings: Optional[
            EventDestinationSettingsDict
        ] = None,
        message_retry_settings: Optional[MessageRetrySettingsDict] = None,
        delivery_report_based_fallback: Optional[
            DeliveryReportBasedFallbackDict
        ] = None,
        *,
        raw_response: Literal[True],
        **kwargs,
    ) -> AppResponse: ...

    def update(
        self,
        app_id: str,
        channel_credentials: Optional[
            ConversationChannelCredentialsDict
        ] = None,
        display_name: Optional[str] = None,
        conversation_metadata_report_view: Optional[
            ConversationMetadataReportViewType
        ] = None,
        retention_policy: Optional[RetentionPolicyDict] = None,
        dispatch_retention_policy: Optional[
            DispatchRetentionPolicyDict
        ] = None,
        processing_mode: Optional[ProcessingModeType] = None,
        smart_conversation: Optional[SmartConversationDict] = None,
        event_destination_settings: Optional[
            EventDestinationSettingsDict
        ] = None,
        message_retry_settings: Optional[MessageRetrySettingsDict] = None,
        delivery_report_based_fallback: Optional[
            DeliveryReportBasedFallbackDict
        ] = None,
        *,
        raw_response: bool = False,
        **kwargs,
    ) -> Union[AppResponse, AppCustomResponse]:
        """
        Updates a particular app as specified by the App ID. Note that this is a
        ``PATCH`` operation, so any specified field values will replace existing values.
        If you'd like to add configurations to an existing app, make sure to include the
        existing values AND the new values in the call (for example, get the app, merge
        your changes into its ``channel_credentials`` map, and send the updated map here).

        :param app_id: The ID of the app to update.
        :type app_id: str
        :param channel_credentials: Channel credentials, keyed by channel. The order of the
            entries defines the app channel priority.
        :type channel_credentials: Optional[ConversationChannelCredentialsDict]
        :param display_name: The display name for the app.
        :type display_name: Optional[str]
        :param conversation_metadata_report_view: Whether conversation metadata is included in reports.
        :type conversation_metadata_report_view: Optional[ConversationMetadataReportViewType]
        :param retention_policy: The retention policy for messages and conversations.
        :type retention_policy: Optional[RetentionPolicyDict]
        :param dispatch_retention_policy: The retention policy for messages in dispatch mode.
        :type dispatch_retention_policy: Optional[DispatchRetentionPolicyDict]
        :param processing_mode: The processing mode for the app.
        :type processing_mode: Optional[ProcessingModeType]
        :param smart_conversation: Smart Conversation settings for the app.
        :type smart_conversation: Optional[SmartConversationDict]
        :param event_destination_settings: Settings for the destination of Sinch events.
        :type event_destination_settings: Optional[EventDestinationSettingsDict]
        :param message_retry_settings: Settings controlling message retry behavior.
        :type message_retry_settings: Optional[MessageRetrySettingsDict]
        :param delivery_report_based_fallback: Delivery-report-based channel fallback settings.
        :type delivery_report_based_fallback: Optional[DeliveryReportBasedFallbackDict]
        :param raw_response: When ``False`` (default) the response exposes ``channel_credentials``
            as a channel-keyed model. Set to ``True`` to get the raw ``AppResponse`` with
            ``channel_credentials`` as the server array.
        :type raw_response: bool
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The updated app.
        :rtype: Union[AppResponse, AppCustomResponse]
        """
        request_data = UpdateAppRequest(
            app_id=app_id,
            channel_credentials=channel_credentials,
            display_name=display_name,
            conversation_metadata_report_view=conversation_metadata_report_view,
            retention_policy=retention_policy,
            dispatch_retention_policy=dispatch_retention_policy,
            processing_mode=processing_mode,
            smart_conversation=smart_conversation,
            event_destination_settings=event_destination_settings,
            message_retry_settings=message_retry_settings,
            delivery_report_based_fallback=delivery_report_based_fallback,
            **kwargs,
        )
        response = self._request(
            UpdateAppEndpoint,
            request_data,
            response_model=AppResponse if raw_response else AppCustomResponse,
        )
        return response

    def delete(self, app_id: str, **kwargs) -> None:
        """
        Deletes the app specified by the App ID. Note that this operation will
        not delete contacts (which are stored at the project level) nor any
        channel-specific resources (for example, WhatsApp Sender Identities will
        not be deleted).

        :param app_id: The ID of the app to delete.
        :type app_id: str
        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = AppIdRequest(app_id=app_id, **kwargs)
        return self._request(DeleteAppEndpoint, request_data)

    @overload
    def get(
        self, app_id: str, *, raw_response: Literal[False] = False, **kwargs
    ) -> AppCustomResponse: ...

    @overload
    def get(
        self, app_id: str, *, raw_response: Literal[True], **kwargs
    ) -> AppResponse: ...

    def get(
        self, app_id: str, *, raw_response: bool = False, **kwargs
    ) -> Union[AppResponse, AppCustomResponse]:
        """
        Returns a particular app as specified by the App ID.

        :param app_id: The ID of the app to retrieve.
        :type app_id: str
        :param raw_response: When ``False`` (default) the response exposes ``channel_credentials``
            as a channel-keyed model. Set to ``True`` to get the raw ``AppResponse`` with
            ``channel_credentials`` as the server array.
        :type raw_response: bool
        :returns: The app details.
        :rtype: Union[AppResponse, AppCustomResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = AppIdRequest(app_id=app_id, **kwargs)
        response = self._request(
            GetAppEndpoint,
            request_data,
            response_model=AppResponse if raw_response else AppCustomResponse,
        )
        return response

    @overload
    def list(
        self, *, raw_response: Literal[False] = False, **kwargs
    ) -> Paginator[AppCustomResponse]: ...

    @overload
    def list(
        self, *, raw_response: Literal[True], **kwargs
    ) -> Paginator[AppResponse]: ...

    def list(
        self, *, raw_response: bool = False, **kwargs
    ) -> Union[Paginator[AppResponse], Paginator[AppCustomResponse]]:
        """
        List all apps for the current project.

        :param raw_response: When ``False`` (default) each app exposes ``channel_credentials``
            as a channel-keyed model. Set to ``True`` to iterate raw ``AppResponse``
            objects with ``channel_credentials`` as the server array.
        :type raw_response: bool
        :returns: A paginator for iterating through the apps.
        :rtype: Union[Paginator[AppResponse], Paginator[AppCustomResponse]]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        response_model = (
            ListAppsResponse if raw_response else ListAppsCustomResponse
        )
        return TokenBasedPaginator(
            sinch=self._sinch,
            endpoint=ListAppsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListAppsRequest(**kwargs),
                response_model=response_model,
            ),
        )
