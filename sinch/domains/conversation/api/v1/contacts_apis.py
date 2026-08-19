from typing import List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.conversation.api.v1.base.base_conversation import (
    BaseConversation,
)
from sinch.domains.conversation.api.v1.internal.contacts_endpoints import (
    CreateContactEndpoint,
    DeleteContactEndpoint,
    GetContactEndpoint,
    ListContactsEndpoint,
    UpdateContactEndpoint,
)
from sinch.domains.conversation.models.v1.contacts.internal.contact_id_request import (
    ContactIdRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.create_contact_request import (
    CreateContactRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.list_contacts_request import (
    ListContactsRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.update_contact_request import (
    UpdateContactRequest,
)
from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.models.v1.contacts.types.contact_language_type import (
    ContactLanguageType,
)
from sinch.domains.conversation.models.v1.types.channel_identity_dict import (
    ChannelIdentityDict,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class Contacts(BaseConversation):
    def list(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        external_id: Optional[str] = None,
        channel: Optional[ConversationChannelType] = None,
        identity: Optional[str] = None,
        **kwargs,
    ) -> Paginator[ContactResponse]:
        """
        List all contacts in the project. Note that, if a WhatsApp contact is returned,
        the ``display_name`` field of that contact may be populated with the WhatsApp
        display name (if the name is already stored on the server and the
        ``display_name`` field has not been overwritten by the user).

        :param page_size: (optional) The maximum number of contacts to fetch. The server
            default is 10 and the maximum is 20.
        :type page_size: Optional[int]
        :param page_token: (optional) Next page token previously returned if any.
        :type page_token: Optional[str]
        :param external_id: (optional) Contact identifier in an external system. If used,
            ``channel`` and ``identity`` can't be used.
        :type external_id: Optional[str]
        :param channel: (optional) Specifies a channel. If set, ``identity`` must be set and
            ``external_id`` can't be used.
        :type channel: Optional[ConversationChannelType]
        :param identity: (optional) If set, ``channel`` must be set and ``external_id`` can't
            be used. Used in conjunction with ``channel`` to uniquely identify the specified
            channel identity.
        :type identity: Optional[str]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: A paginator for iterating through the contacts.
        :rtype: Paginator[ContactResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return TokenBasedPaginator(
            sinch=self._sinch,
            endpoint=ListContactsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListContactsRequest(
                    page_size=page_size,
                    page_token=page_token,
                    external_id=external_id,
                    channel=channel,
                    identity=identity,
                    **kwargs,
                ),
            ),
        )

    def create(
        self,
        channel_identities: List[ChannelIdentityDict],
        language: ContactLanguageType,
        channel_priority: UnsetOr[
            Optional[List[ConversationChannelType]]
        ] = UNSET,
        display_name: UnsetOr[Optional[str]] = UNSET,
        email: UnsetOr[Optional[str]] = UNSET,
        external_id: UnsetOr[Optional[str]] = UNSET,
        metadata: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> ContactResponse:
        """
        Most Conversation API contacts are created automatically when a message is sent to
        a new recipient. You can also create a new contact manually using this API call.

        :param channel_identities: (required) List of channel identities. Must contain at
            least one item.
        :type channel_identities: List[ChannelIdentityDict]
        :param language: (required) The language of the contact.
        :type language: ContactLanguageType
        :param channel_priority: (optional) List of channels defining the channel priority.
            The channel at the top of the list is tried first.
        :type channel_priority: UnsetOr[Optional[List[ConversationChannelType]]]
        :param display_name: (optional) The display name. A default 'Unknown' will be
            assigned by the server if left empty.
        :type display_name: UnsetOr[Optional[str]]
        :param email: (optional) Email of the contact.
        :type email: UnsetOr[Optional[str]]
        :param external_id: (optional) Contact identifier in an external system.
        :type external_id: UnsetOr[Optional[str]]
        :param metadata: (optional) Metadata associated with the contact. Up to 1024
            characters long.
        :type metadata: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The created contact.
        :rtype: ContactResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = CreateContactRequest(
            channel_identities=channel_identities,
            language=language,
            **strip_unset(
                {
                    "channel_priority": channel_priority,
                    "display_name": display_name,
                    "email": email,
                    "external_id": external_id,
                    "metadata": metadata,
                }
            ),
            **kwargs,
        )
        return self._request(CreateContactEndpoint, request_data)

    def get(self, contact_id: str, **kwargs) -> ContactResponse:
        """
        Returns a specific contact as specified by the contact ID. Note the following:

        - If a WhatsApp contact is returned, the ``display_name`` field of that contact may
          be populated with the WhatsApp display name (if the name is already stored on the
          server and the ``display_name`` field has not been overwritten by the user).

        - If you receive an Inbound Message callback for an MO message on the Instagram
          channel, the corresponding payload will not include the Instagram username. You
          may use the ``contact_id`` and ``channel_identity`` values included in the callback
          to retrieve the username (detailed in the ``display_name`` field) with this
          operation.

        :param contact_id: (required) The unique ID of the contact to retrieve.
        :type contact_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The contact details.
        :rtype: ContactResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = ContactIdRequest(contact_id=contact_id, **kwargs)
        return self._request(GetContactEndpoint, request_data)

    def delete(self, contact_id: str, **kwargs) -> None:
        """
        Delete a contact as specified by the contact ID.

        :param contact_id: (required) The unique ID of the contact to delete.
        :type contact_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = ContactIdRequest(contact_id=contact_id, **kwargs)
        return self._request(DeleteContactEndpoint, request_data)

    def update(
        self,
        contact_id: str,
        channel_identities: UnsetOr[
            Optional[List[ChannelIdentityDict]]
        ] = UNSET,
        channel_priority: UnsetOr[
            Optional[List[ConversationChannelType]]
        ] = UNSET,
        display_name: UnsetOr[Optional[str]] = UNSET,
        email: UnsetOr[Optional[str]] = UNSET,
        external_id: UnsetOr[Optional[str]] = UNSET,
        language: UnsetOr[ContactLanguageType] = UNSET,
        metadata: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> ContactResponse:
        """
        Updates a contact as specified by the contact ID.

        Omitted parameters are left untouched on the server; passing ``None``
        explicitly clears the field.

        :param contact_id: (required) The unique ID of the contact to update.
        :type contact_id: str
        :param channel_identities: (optional) List of channel identities.
        :type channel_identities: UnsetOr[Optional[List[ChannelIdentityDict]]]
        :param channel_priority: (optional) List of channels defining the channel priority.
        :type channel_priority: UnsetOr[Optional[List[ConversationChannelType]]]
        :param display_name: (optional) The display name of the contact.
        :type display_name: UnsetOr[Optional[str]]
        :param email: (optional) Email of the contact.
        :type email: UnsetOr[Optional[str]]
        :param external_id: (optional) Contact identifier in an external system.
        :type external_id: UnsetOr[Optional[str]]
        :param language: (optional) The language of the contact.
        :type language: UnsetOr[ContactLanguageType]
        :param metadata: (optional) Metadata associated with the contact. Up to 1024
            characters long.
        :type metadata: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The updated contact.
        :rtype: ContactResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = UpdateContactRequest(
            contact_id=contact_id,
            **strip_unset(
                {
                    "channel_identities": channel_identities,
                    "channel_priority": channel_priority,
                    "display_name": display_name,
                    "email": email,
                    "external_id": external_id,
                    "language": language,
                    "metadata": metadata,
                }
            ),
            **kwargs,
        )
        return self._request(UpdateContactEndpoint, request_data)
