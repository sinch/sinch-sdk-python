from sinch.domains.conversation.models.contact.responses import (
    ListConversationContactsResponse,
    GetConversationContactResponse
)


def test_get_contact(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    get_contact_response = sinch_client_sync.conversation.contact.get(
        contact_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(get_contact_response, GetConversationContactResponse)


async def test_get_contact_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    get_contact_response = await sinch_client_async.conversation.contact.get(
        contact_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(get_contact_response, GetConversationContactResponse)
