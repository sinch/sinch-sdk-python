from sinch.domains.conversation.models.message.responses import GetConversationMessageResponse


def test_get_message(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_messages_response = sinch_client_sync.conversation.message.list(
        contact_id=list_contacts_response.result.contacts[0].id
    )
    get_message_response = sinch_client_sync.conversation.message.get(
        message_id=list_messages_response.result.messages[0].id
    )
    assert isinstance(get_message_response, GetConversationMessageResponse)


async def test_get_message_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    list_messages_response = await sinch_client_async.conversation.message.list(
        contact_id=list_contacts_response.result.contacts[0].id
    )
    get_message_response = await sinch_client_async.conversation.message.get(
        message_id=list_messages_response.result.messages[0].id
    )
    assert isinstance(get_message_response, GetConversationMessageResponse)
