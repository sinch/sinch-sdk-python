from sinch.domains.conversation.models.message.responses import DeleteConversationMessageResponse


def test_delete_message(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_messages_response = sinch_client_sync.conversation.message.list(
        contact_id=list_contacts_response.result.contacts[0].id
    )
    delete_message_response = sinch_client_sync.conversation.message.delete(
        message_id=list_messages_response.result.messages[0].id
    )
    assert isinstance(delete_message_response, DeleteConversationMessageResponse)


async def test_delete_message_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    list_messages_response = await sinch_client_async.conversation.message.list(
        contact_id=list_contacts_response.result.contacts[0].id
    )
    delete_message_response = await sinch_client_async.conversation.message.delete(
        message_id=list_messages_response.result.messages[0].id
    )
    assert isinstance(delete_message_response, DeleteConversationMessageResponse)
