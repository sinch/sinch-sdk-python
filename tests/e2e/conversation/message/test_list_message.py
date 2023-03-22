from sinch.domains.conversation.models.message.responses import ListConversationMessagesResponse


def test_list_message(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_messages_response = sinch_client_sync.conversation.message.list(
        contact_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(list_messages_response.result, ListConversationMessagesResponse)


async def test_list_message_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    list_messages_response = await sinch_client_async.conversation.message.list(
        contact_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(list_messages_response.result, ListConversationMessagesResponse)
