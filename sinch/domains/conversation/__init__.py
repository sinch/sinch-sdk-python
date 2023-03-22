from typing import List

from sinch.core.pagination import TokenBasedPaginator, AsyncTokenBasedPaginator

from sinch.domains.conversation.models import (
    SinchConversationChannelIdentities,
    SinchConversationRecipient,
    ConversationChannel
)

from sinch.domains.conversation.models.app.requests import (
    CreateConversationAppRequest,
    DeleteConversationAppRequest,
    GetConversationAppRequest,
    UpdateConversationAppRequest
)

from sinch.domains.conversation.models.app.responses import (
    CreateConversationAppResponse,
    DeleteConversationAppResponse,
    ListConversationAppsResponse,
    GetConversationAppResponse,
    UpdateConversationAppResponse
)

from sinch.domains.conversation.models.contact.requests import (
    CreateConversationContactRequest,
    UpdateConversationContactRequest,
    ListConversationContactRequest,
    DeleteConversationContactRequest,
    GetConversationContactRequest,
    MergeConversationContactsRequest,
    GetConversationChannelProfileRequest
)

from sinch.domains.conversation.models.contact.responses import (
    UpdateConversationContactResponse,
    ListConversationContactsResponse,
    DeleteConversationContactResponse,
    MergeConversationContactsResponse,
    CreateConversationContactResponse,
    GetConversationContactResponse,
    GetConversationChannelProfileResponse
)

from sinch.domains.conversation.models.message.requests import (
    SendConversationMessageRequest,
    ListConversationMessagesRequest,
    DeleteConversationMessageRequest,
    GetConversationMessageRequest
)

from sinch.domains.conversation.models.message.responses import (
    SendConversationMessageResponse,
    ListConversationMessagesResponse,
    GetConversationMessageResponse,
    DeleteConversationMessageResponse
)

from sinch.domains.conversation.models.conversation.requests import (
    CreateConversationRequest,
    ListConversationsRequest,
    GetConversationRequest,
    DeleteConversationRequest,
    UpdateConversationRequest,
    StopConversationRequest,
    InjectMessageToConversationRequest
)

from sinch.domains.conversation.models.conversation.responses import (
    SinchCreateConversationResponse,
    SinchUpdateConversationResponse,
    SinchGetConversationResponse,
    SinchDeleteConversationResponse,
    SinchListConversationsResponse,
    SinchStopConversationResponse,
    SinchInjectMessageResponse
)

from sinch.domains.conversation.models.webhook.requests import (
    CreateConversationWebhookRequest,
    GetConversationWebhookRequest,
    DeleteConversationWebhookRequest,
    UpdateConversationWebhookRequest,
    ListConversationWebhookRequest
)

from sinch.domains.conversation.models.webhook.responses import (
    CreateWebhookResponse,
    GetWebhookResponse,
    SinchListWebhooksResponse,
    SinchDeleteWebhookResponse,
    UpdateWebhookResponse
)

from sinch.domains.conversation.models.templates.requests import (
    CreateConversationTemplateRequest,
    GetConversationTemplateRequest,
    DeleteConversationTemplateRequest,
    UpdateConversationTemplateRequest
)

from sinch.domains.conversation.models.templates.responses import (
    CreateConversationTemplateResponse,
    UpdateConversationTemplateResponse,
    DeleteConversationTemplateResponse,
    ListConversationTemplatesResponse,
    GetConversationTemplateResponse
)

from sinch.domains.conversation.models.event.requests import SendConversationEventRequest
from sinch.domains.conversation.models.event.responses import SendConversationEventResponse

from sinch.domains.conversation.models.opt_in_opt_out.requests import RegisterConversationOptInRequest
from sinch.domains.conversation.models.opt_in_opt_out.responses import RegisterConversationOptInResponse

from sinch.domains.conversation.models.opt_in_opt_out.requests import RegisterConversationOptOutRequest
from sinch.domains.conversation.models.opt_in_opt_out.responses import RegisterConversationOptOutResponse

from sinch.domains.conversation.models.capability.requests import QueryConversationCapabilityRequest
from sinch.domains.conversation.models.capability.responses import QueryConversationCapabilityResponse

from sinch.domains.conversation.models.transcoding.requests import TranscodeConversationMessageRequest
from sinch.domains.conversation.models.transcoding.responses import TranscodeConversationMessageResponse

from sinch.domains.conversation.endpoints.message.send_message import SendConversationMessageEndpoint
from sinch.domains.conversation.endpoints.message.list_message import ListConversationMessagesEndpoint
from sinch.domains.conversation.endpoints.message.get_message import GetConversationMessageEndpoint
from sinch.domains.conversation.endpoints.message.delete_message import DeleteConversationMessageEndpoint
from sinch.domains.conversation.endpoints.contact.list_contact import ListContactsEndpoint
from sinch.domains.conversation.endpoints.contact.create_contact import CreateConversationContactEndpoint
from sinch.domains.conversation.endpoints.contact.get_contact import GetContactEndpoint
from sinch.domains.conversation.endpoints.contact.delete_contact import DeleteContactEndpoint
from sinch.domains.conversation.endpoints.contact.update_contact import UpdateConversationContactEndpoint
from sinch.domains.conversation.endpoints.contact.merge_contacts import MergeConversationContactsEndpoint
from sinch.domains.conversation.endpoints.contact.get_channel_profile import GetChannelProfileEndpoint
from sinch.domains.conversation.endpoints.app.create_app import CreateConversationAppEndpoint
from sinch.domains.conversation.endpoints.app.delete_app import DeleteConversationAppEndpoint
from sinch.domains.conversation.endpoints.app.list_apps import ListAppsEndpoint
from sinch.domains.conversation.endpoints.app.get_app import GetAppEndpoint
from sinch.domains.conversation.endpoints.app.update_app import UpdateConversationAppEndpoint
from sinch.domains.conversation.endpoints.conversation.create_conversation import CreateConversationEndpoint
from sinch.domains.conversation.endpoints.conversation.list_conversations import ListConversationsEndpoint
from sinch.domains.conversation.endpoints.conversation.get_conversation import GetConversationEndpoint
from sinch.domains.conversation.endpoints.conversation.delete_conversation import DeleteConversationEndpoint
from sinch.domains.conversation.endpoints.conversation.update_conversation import UpdateConversationEndpoint
from sinch.domains.conversation.endpoints.conversation.stop_conversation import StopConversationEndpoint
from sinch.domains.conversation.endpoints.conversation.inject_message_to_conversation import (
    InjectMessageToConversationEndpoint
)
from sinch.domains.conversation.endpoints.webhooks.create_webhook import CreateWebhookEndpoint
from sinch.domains.conversation.endpoints.webhooks.list_webhooks import ListWebhooksEndpoint
from sinch.domains.conversation.endpoints.webhooks.get_webhook import GetWebhookEndpoint
from sinch.domains.conversation.endpoints.webhooks.delete_webhook import DeleteWebhookEndpoint
from sinch.domains.conversation.endpoints.webhooks.update_webhook import UpdateWebhookEndpoint
from sinch.domains.conversation.endpoints.templates.create_template import CreateTemplateEndpoint
from sinch.domains.conversation.endpoints.templates.list_templates import ListTemplatesEndpoint
from sinch.domains.conversation.endpoints.templates.get_template import GetTemplatesEndpoint
from sinch.domains.conversation.endpoints.templates.delete_template import DeleteTemplateEndpoint
from sinch.domains.conversation.endpoints.templates.update_template import UpdateTemplateEndpoint
from sinch.domains.conversation.endpoints.events import SendEventEndpoint
from sinch.domains.conversation.endpoints.transcode import TranscodeMessageEndpoint
from sinch.domains.conversation.endpoints.opt_in import RegisterOptInEndpoint
from sinch.domains.conversation.endpoints.opt_out import RegisterOptOutEndpoint
from sinch.domains.conversation.endpoints.capability import CapabilityQueryEndpoint


class ConversationMessage:
    def __init__(self, sinch):
        self._sinch = sinch

    def send(
        self,
        app_id: str,
        recipient: dict,
        message: dict,
        callback_url: str = None,
        channel_priority_order: list = None,
        channel_properties: dict = None,
        message_metadata: str = None,
        conversation_metadata: dict = None,
        queue: str = None,
        ttl: str = None,
        processing_strategy: str = None
    ) -> SendConversationMessageResponse:
        return self._sinch.configuration.transport.request(
            SendConversationMessageEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=SendConversationMessageRequest(
                    app_id=app_id,
                    recipient=recipient,
                    message=message,
                    callback_url=callback_url,
                    channel_priority_order=channel_priority_order,
                    channel_properties=channel_properties,
                    message_metadata=message_metadata,
                    conversation_metadata=conversation_metadata,
                    queue=queue,
                    ttl=ttl,
                    processing_strategy=processing_strategy
                )
            )
        )

    def get(
        self,
        message_id: str,
        messages_source: str = None
    ) -> GetConversationMessageResponse:
        return self._sinch.configuration.transport.request(
            GetConversationMessageEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetConversationMessageRequest(
                    message_id=message_id,
                    messages_source=messages_source
                )
            )
        )

    def delete(
        self,
        message_id: str,
        messages_source: str = None
    ) -> DeleteConversationMessageResponse:
        return self._sinch.configuration.transport.request(
            DeleteConversationMessageEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=DeleteConversationMessageRequest(
                    message_id=message_id,
                    messages_source=messages_source
                )
            )
        )

    def list(
        self,
        conversation_id: str = None,
        contact_id: str = None,
        app_id: str = None,
        page_size: int = None,
        page_token: str = None,
        view: str = None,
        messages_source: str = None,
        only_recipient_originated: bool = None
    ) -> ListConversationMessagesResponse:
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListConversationMessagesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListConversationMessagesRequest(
                    contact_id=contact_id,
                    conversation_id=conversation_id,
                    app_id=app_id,
                    page_size=page_size,
                    page_token=page_token,
                    view=view,
                    messages_source=messages_source,
                    only_recipient_originated=only_recipient_originated
                )
            )
        )


class ConversationMessageWithAsyncPagination(ConversationMessage):
    async def list(
        self,
        conversation_id: str = None,
        contact_id: str = None,
        app_id: str = None,
        page_size: int = None,
        page_token: str = None,
        view: str = None,
        messages_source: str = None,
        only_recipient_originated: bool = None
    ) -> ListConversationMessagesResponse:
        return await AsyncTokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListConversationMessagesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListConversationMessagesRequest(
                    contact_id=contact_id,
                    conversation_id=conversation_id,
                    app_id=app_id,
                    page_size=page_size,
                    page_token=page_token,
                    view=view,
                    messages_source=messages_source,
                    only_recipient_originated=only_recipient_originated
                )
            )
        )


class ConversationApp:
    def __init__(self, sinch):
        self._sinch = sinch

    def create(
        self,
        display_name: str,
        channel_credentials: list,
        conversation_metadata_report_view: str = None,
        retention_policy: dict = None,
        dispatch_retention_policy: dict = None,
        processing_mode: str = None
    ) -> CreateConversationAppResponse:
        """
        Creates a new Conversation API app with one or more configured channels.
        The ID of the app is generated at creation and is returned in the response.
        https://developers.sinch.com/docs/conversation/api-reference/conversation/tag/App/#tag/App/operation/App_CreateApp
        """
        return self._sinch.configuration.transport.request(
            CreateConversationAppEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=CreateConversationAppRequest(
                    display_name=display_name,
                    channel_credentials=channel_credentials,
                    conversation_metadata_report_view=conversation_metadata_report_view,
                    retention_policy=retention_policy,
                    dispatch_retention_policy=dispatch_retention_policy,
                    processing_mode=processing_mode
                )
            )
        )

    def delete(self, app_id: str) -> DeleteConversationAppResponse:
        """
        Deletes the app identified by the app_id.
        """
        return self._sinch.configuration.transport.request(
            DeleteConversationAppEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=DeleteConversationAppRequest(app_id)
            )
        )

    def list(self) -> ListConversationAppsResponse:
        """
        Lists all apps for the project identified by the project_id.
        Returns the information as an array of app objects in the response.
        """
        return self._sinch.configuration.transport.request(
            ListAppsEndpoint(
                project_id=self._sinch.configuration.project_id
            )
        )

    def get(self, app_id: str) -> GetConversationAppResponse:
        """
        Returns the configuration information of the app, specified by the app_id, in the response.
        """
        return self._sinch.configuration.transport.request(
            GetAppEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetConversationAppRequest(
                    app_id=app_id
                )
            )
        )

    def update(
        self,
        app_id: str,
        display_name: str,
        channel_credentials: list = None,
        update_mask=None,
        conversation_metadata_report_view=None,
        retention_policy=None,
        dispatch_retention_policy=None,
        processing_mode=None
    ) -> UpdateConversationAppResponse:
        """
        Updates an existing Conversation API app with new configuration options defined in the request.
        The details of the updated app are returned in the response.
        """
        return self._sinch.configuration.transport.request(
            UpdateConversationAppEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=UpdateConversationAppRequest(
                    app_id=app_id,
                    display_name=display_name,
                    channel_credentials=channel_credentials,
                    update_mask=update_mask,
                    conversation_metadata_report_view=conversation_metadata_report_view,
                    retention_policy=retention_policy,
                    dispatch_retention_policy=dispatch_retention_policy,
                    processing_mode=processing_mode
                )
            )
        )


class ConversationContact:
    def __init__(self, sinch):
        self._sinch = sinch

    def update(
        self,
        contact_id: str,
        channel_identities: List[SinchConversationChannelIdentities] = None,
        language: str = None,
        display_name: str = None,
        email: str = None,
        external_id: str = None,
        metadata: str = None,
        channel_priority: list = None
    ) -> UpdateConversationContactResponse:
        """
        Updates an existing Conversation API contact with new configuration options defined in the request.
        The details of the updated contact are returned in the response.
        """
        return self._sinch.configuration.transport.request(
            UpdateConversationContactEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=UpdateConversationContactRequest(
                    channel_identities=channel_identities,
                    language=language,
                    display_name=display_name,
                    email=email,
                    external_id=external_id,
                    metadata=metadata,
                    channel_priority=channel_priority,
                    id=contact_id
                )
            )
        )

    def create(
        self,
        channel_identities: List[SinchConversationChannelIdentities],
        language: str,
        display_name: str = None,
        email: str = None,
        external_id: str = None,
        metadata: str = None,
        channel_priority: list = None
    ) -> CreateConversationContactResponse:
        """
        Creates a new Conversation API contact.
        The ID of the contact is generated at creation and is returned in the response.
        """
        return self._sinch.configuration.transport.request(
            CreateConversationContactEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=CreateConversationContactRequest(
                    channel_identities=channel_identities,
                    language=language,
                    display_name=display_name,
                    email=email,
                    external_id=external_id,
                    metadata=metadata,
                    channel_priority=channel_priority
                )
            )
        )

    def delete(self, contact_id: str) -> DeleteConversationContactResponse:
        """
        Deletes the Conversation API contact identified by the contact_id.
        """
        return self._sinch.configuration.transport.request(
            DeleteContactEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=DeleteConversationContactRequest(
                    contact_id=contact_id
                )
            )
        )

    def get(self, contact_id: str) -> GetConversationContactResponse:
        """
        Returns the configuration information of the
        Conversation API contact, specified by the contact_id, in the response.
        """
        return self._sinch.configuration.transport.request(
            GetContactEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetConversationContactRequest(
                    contact_id=contact_id
                )
            )
        )

    def list(
        self,
        page_size: int = None,
        page_token: str = None,
        external_id: str = None,
        channel: str = None,
        identity: str = None
    ) -> ListConversationContactsResponse:
        """
        Lists all Conversation API contacts for the project identified by the project_id.
        Returns the information as an array of contact objects in the response.
        """
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListContactsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListConversationContactRequest(
                    page_size=page_size,
                    page_token=page_token,
                    external_id=external_id,
                    channel=channel,
                    identity=identity
                )
            )
        )

    def merge(
        self,
        source_id: str,
        destination_id: str,
        strategy: str = None
    ) -> MergeConversationContactsResponse:
        """
        Merges two existing Conversation API contacts.
        The contact specified by the destination_id will be kept.
        The contact specified by the source_id will be deleted.
        All conversations from source contact are merged into destination.
        Channel identities and optional fields from source contact are only
        merged if corresponding entries do not exist in destination.
        """
        return self._sinch.configuration.transport.request(
            MergeConversationContactsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=MergeConversationContactsRequest(
                    destination_id=destination_id,
                    strategy=strategy,
                    source_id=source_id
                )
            )
        )

    def get_channel_profile(
        self,
        app_id: str,
        recipient: SinchConversationRecipient,
        channel: ConversationChannel,
    ) -> GetConversationChannelProfileResponse:
        """
        Returns the user profile information for the specified recipient on the specified channel.
        This request is not supported for all Conversation API channels.
        """
        return self._sinch.configuration.transport.request(
            GetChannelProfileEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetConversationChannelProfileRequest(
                    app_id=app_id,
                    recipient=recipient,
                    channel=channel
                )
            )
        )


class ConversationContactWithAsyncPagination(ConversationContact):
    async def list(
        self,
        page_size: int = None,
        page_token: str = None,
        external_id: str = None,
        channel: str = None,
        identity: str = None
    ) -> ListConversationContactsResponse:
        return await AsyncTokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListContactsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListConversationContactRequest(
                    page_size=page_size,
                    page_token=page_token,
                    external_id=external_id,
                    channel=channel,
                    identity=identity
                )
            )
        )


class ConversationEvent:
    def __init__(self, sinch):
        self._sinch = sinch

    def send(
        self,
        app_id: str,
        recipient: dict,
        event: dict,
        callback_url: str = None,
        channel_priority_order: str = None,
        event_metadata: str = None,
        queue: str = None
    ) -> SendConversationEventResponse:
        return self._sinch.configuration.transport.request(
            SendEventEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=SendConversationEventRequest(
                    app_id=app_id,
                    recipient=recipient,
                    event=event,
                    callback_url=callback_url,
                    channel_priority_order=channel_priority_order,
                    event_metadata=event_metadata,
                    queue=queue
                )
            )
        )


class ConversationTranscoding:
    def __init__(self, sinch):
        self._sinch = sinch

    def transcode_message(
        self,
        app_id: str,
        app_message: dict,
        channels: list,
        from_: str = None,
        to: str = None
    ) -> TranscodeConversationMessageResponse:
        return self._sinch.configuration.transport.request(
            TranscodeMessageEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=TranscodeConversationMessageRequest(
                    app_id=app_id,
                    app_message=app_message,
                    channels=channels,
                    from_=from_,
                    to=to
                )
            )
        )


class ConversationOptIn:
    def __init__(self, sinch):
        self._sinch = sinch

    def register(
        self,
        app_id: str,
        channels: list,
        recipient: dict,
        request_id: str = None,
        processing_strategy: str = None
    ) -> RegisterConversationOptInResponse:
        return self._sinch.configuration.transport.request(
            RegisterOptInEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=RegisterConversationOptInRequest(
                    app_id=app_id,
                    recipient=recipient,
                    channels=channels,
                    request_id=request_id,
                    processing_strategy=processing_strategy
                )
            )
        )


class ConversationOptOut:
    def __init__(self, sinch):
        self._sinch = sinch

    def register(
        self,
        app_id: str,
        channels: list,
        recipient: dict,
        request_id: str = None,
        processing_strategy: str = None
    ) -> RegisterConversationOptOutResponse:
        return self._sinch.configuration.transport.request(
            RegisterOptOutEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=RegisterConversationOptOutRequest(
                    app_id=app_id,
                    recipient=recipient,
                    channels=channels,
                    request_id=request_id,
                    processing_strategy=processing_strategy
                )
            )
        )


class ConversationCapability:
    def __init__(self, sinch):
        self._sinch = sinch

    def query(
        self,
        app_id: str,
        recipient: dict,
        request_id: str = None
    ) -> QueryConversationCapabilityResponse:
        return self._sinch.configuration.transport.request(
            CapabilityQueryEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=QueryConversationCapabilityRequest(
                    app_id=app_id,
                    recipient=recipient,
                    request_id=request_id
                )
            )
        )


class ConversationTemplate:
    def __init__(self, sinch):
        self._sinch = sinch

    def create(
        self,
        translations: list,
        default_translation: str,
        channel: str = None,
        create_time: str = None,
        description: str = None,
        id: str = None,
        update_time: str = None
    ) -> CreateConversationTemplateResponse:
        return self._sinch.configuration.transport.request(
            CreateTemplateEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=CreateConversationTemplateRequest(
                    channel=channel,
                    create_time=create_time,
                    description=description,
                    id=id,
                    translations=translations,
                    default_translation=default_translation,
                    update_time=update_time
                )
            )
        )

    def list(self) -> ListConversationTemplatesResponse:
        return self._sinch.configuration.transport.request(
            ListTemplatesEndpoint(
                project_id=self._sinch.configuration.project_id
            )
        )

    def get(self, template_id: str) -> GetConversationTemplateResponse:
        return self._sinch.configuration.transport.request(
            GetTemplatesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetConversationTemplateRequest(
                    template_id=template_id
                )
            )
        )

    def update(
        self,
        template_id: str,
        translations: list,
        default_translation: str,
        id: str = None,
        update_mask: str = None,
        channel: str = None,
        create_time: str = None,
        description: str = None,
        update_time: str = None
    ) -> UpdateConversationTemplateResponse:
        return self._sinch.configuration.transport.request(
            UpdateTemplateEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=UpdateConversationTemplateRequest(
                    channel=channel,
                    create_time=create_time,
                    description=description,
                    id=id,
                    translations=translations,
                    default_translation=default_translation,
                    update_time=update_time,
                    update_mask=update_mask,
                    template_id=template_id
                )
            )
        )

    def delete(self, template_id: str) -> DeleteConversationTemplateResponse:
        return self._sinch.configuration.transport.request(
            DeleteTemplateEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=DeleteConversationTemplateRequest(
                    template_id=template_id
                )
            )
        )


class ConversationWebhook:
    def __init__(self, sinch):
        self._sinch = sinch

    def create(
        self,
        app_id: str,
        target: str,
        triggers: list,
        client_credentials: dict = None,
        secret: str = None,
        target_type: str = None
    ) -> CreateWebhookResponse:
        return self._sinch.configuration.transport.request(
            CreateWebhookEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=CreateConversationWebhookRequest(
                    app_id=app_id,
                    target=target,
                    triggers=triggers,
                    client_credentials=client_credentials,
                    secret=secret,
                    target_type=target_type
                )
            )
        )

    def update(
        self,
        webhook_id: str,
        app_id: str,
        target: str,
        triggers: list,
        update_mask: str = None,
        client_credentials: dict = None,
        secret: str = None,
        target_type: str = None
    ) -> UpdateWebhookResponse:
        return self._sinch.configuration.transport.request(
            UpdateWebhookEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=UpdateConversationWebhookRequest(
                    app_id=app_id,
                    target=target,
                    triggers=triggers,
                    client_credentials=client_credentials,
                    secret=secret,
                    target_type=target_type,
                    update_mask=update_mask,
                    webhook_id=webhook_id
                )
            )
        )

    def list(self, app_id: str) -> SinchListWebhooksResponse:
        return self._sinch.configuration.transport.request(
            ListWebhooksEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListConversationWebhookRequest(
                    app_id=app_id
                )
            )
        )

    def get(self, webhook_id: str) -> GetWebhookResponse:
        return self._sinch.configuration.transport.request(
            GetWebhookEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetConversationWebhookRequest(
                    webhook_id=webhook_id
                )
            )
        )

    def delete(self, webhook_id: str) -> SinchDeleteWebhookResponse:
        return self._sinch.configuration.transport.request(
            DeleteWebhookEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=DeleteConversationWebhookRequest(
                    webhook_id=webhook_id
                )
            )
        )


class ConversationConversation:
    def __init__(self, sinch):
        self._sinch = sinch

    def create(
        self,
        id: str = None,
        metadata: str = None,
        conversation_metadata: dict = None,
        contact_id: str = None,
        app_id: str = None,
        active_channel: str = None,
        active: bool = None,
    ) -> SinchCreateConversationResponse:
        return self._sinch.configuration.transport.request(
            CreateConversationEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=CreateConversationRequest(
                    app_id=app_id,
                    contact_id=contact_id,
                    id=id,
                    metadata=metadata,
                    conversation_metadata=conversation_metadata,
                    active_channel=active_channel,
                    active=active
                )
            )
        )

    def list(
        self,
        only_active: bool,
        page_size: int = None,
        page_token: str = None,
        app_id: str = None,
        contact_id: str = None
    ) -> SinchListConversationsResponse:
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListConversationsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListConversationsRequest(
                    only_active=only_active,
                    page_size=page_size,
                    page_token=page_token,
                    app_id=app_id,
                    contact_id=contact_id
                )
            )
        )

    def get(self, conversation_id: str) -> SinchGetConversationResponse:
        return self._sinch.configuration.transport.request(
            GetConversationEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetConversationRequest(
                    conversation_id=conversation_id
                )
            )
        )

    def delete(self, conversation_id: str) -> SinchDeleteConversationResponse:
        return self._sinch.configuration.transport.request(
            DeleteConversationEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=DeleteConversationRequest(
                    conversation_id=conversation_id
                )
            )
        )

    def update(
        self,
        conversation_id: str,
        update_mask: str = None,
        metadata_update_strategy: str = None,
        metadata: str = None,
        conversation_metadata: dict = None,
        contact_id: str = None,
        app_id: str = None,
        active_channel: str = None,
        active: bool = None
    ) -> SinchUpdateConversationResponse:
        return self._sinch.configuration.transport.request(
            UpdateConversationEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=UpdateConversationRequest(
                    app_id=app_id,
                    contact_id=contact_id,
                    conversation_id=conversation_id,
                    metadata=metadata,
                    conversation_metadata=conversation_metadata,
                    active_channel=active_channel,
                    active=active,
                    metadata_update_strategy=metadata_update_strategy,
                    update_mask=update_mask
                )
            )
        )

    def stop(self, conversation_id: str) -> SinchStopConversationResponse:
        return self._sinch.configuration.transport.request(
            StopConversationEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=StopConversationRequest(
                    conversation_id=conversation_id
                )
            )
        )

    def inject_message_to_conversation(
        self,
        conversation_id: str,
        accept_time: str = None,
        app_message: dict = None,
        channel_identity: dict = None,
        contact_id: str = None,
        contact_message: dict = None,
        direction: str = None,
        metadata: str = None
    ) -> SinchInjectMessageResponse:
        return self._sinch.configuration.transport.request(
            InjectMessageToConversationEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=InjectMessageToConversationRequest(
                    conversation_id=conversation_id,
                    accept_time=accept_time,
                    app_message=app_message,
                    channel_identity=channel_identity,
                    contact_id=contact_id,
                    contact_message=contact_message,
                    direction=direction,
                    metadata=metadata
                )
            )
        )


class ConversationConversationWithAsyncPagination(ConversationConversation):
    async def list(
        self,
        only_active: bool,
        page_size: int = None,
        page_token: str = None,
        app_id: str = None,
        contact_id: str = None
    ) -> SinchListConversationsResponse:
        return await AsyncTokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListConversationsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListConversationsRequest(
                    only_active=only_active,
                    page_size=page_size,
                    page_token=page_token,
                    app_id=app_id,
                    contact_id=contact_id
                )
            )
        )


class ConversationBase:
    """
    Documentation for the Conversation API: https://developers.sinch.com/docs/conversation/
    """

    def __init__(self, sinch):
        self._sinch = sinch


class Conversation(ConversationBase):
    """
    Synchronous version of the Conversation Domain
    """
    __doc__ += ConversationBase.__doc__

    def __init__(self, sinch):
        super(Conversation, self).__init__(sinch)
        self.message = ConversationMessage(self._sinch)
        self.app = ConversationApp(self._sinch)
        self.contact = ConversationContact(self._sinch)
        self.event = ConversationEvent(self._sinch)
        self.transcoding = ConversationTranscoding(self._sinch)
        self.opt_in = ConversationOptIn(self._sinch)
        self.opt_out = ConversationOptOut(self._sinch)
        self.capability = ConversationCapability(self._sinch)
        self.template = ConversationTemplate(self._sinch)
        self.webhook = ConversationWebhook(self._sinch)
        self.conversation = ConversationConversation(self._sinch)


class ConversationAsync(ConversationBase):
    """
    Asynchronous version of the Conversation Domain
    """
    __doc__ += ConversationBase.__doc__

    def __init__(self, sinch):
        super(ConversationAsync, self).__init__(sinch)
        self.message = ConversationMessageWithAsyncPagination(self._sinch)
        self.app = ConversationApp(self._sinch)
        self.contact = ConversationContactWithAsyncPagination(self._sinch)
        self.event = ConversationEvent(self._sinch)
        self.transcoding = ConversationTranscoding(self._sinch)
        self.opt_in = ConversationOptIn(self._sinch)
        self.opt_out = ConversationOptOut(self._sinch)
        self.capability = ConversationCapability(self._sinch)
        self.template = ConversationTemplate(self._sinch)
        self.webhook = ConversationWebhook(self._sinch)
        self.conversation = ConversationConversationWithAsyncPagination(self._sinch)
