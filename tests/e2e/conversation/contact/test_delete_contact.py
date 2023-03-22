from sinch.domains.conversation.models.contact.responses import ListConversationContactsResponse, DeleteConversationContactResponse


def test_delete_contact(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    delete_contact_response = sinch_client_sync.conversation.contact.delete(
        contact_id=list_contacts_response.result.contacts[-1].id
    )
    assert isinstance(delete_contact_response, DeleteConversationContactResponse)


async def test_delete_contact_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    delete_contact_response = await sinch_client_async.conversation.contact.delete(
        contact_id=list_contacts_response.result.contacts[-1].id
    )
    assert isinstance(delete_contact_response, DeleteConversationContactResponse)
