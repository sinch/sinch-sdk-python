from sinch.domains.conversation.models.conversation.responses import SinchDeleteConversationResponse


def test_delete_conversation(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_conversations_response = sinch_client_sync.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )

    delete_conversation_response = sinch_client_sync.conversation.conversation.delete(
        conversation_id=list_conversations_response.result.conversations[-1].id
    )
    assert isinstance(delete_conversation_response, SinchDeleteConversationResponse)


async def test_delete_conversation_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    list_conversations_response = await sinch_client_async.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )

    delete_conversation_response = await sinch_client_async.conversation.conversation.delete(
        conversation_id=list_conversations_response.result.conversations[-1].id
    )
    assert isinstance(delete_conversation_response, SinchDeleteConversationResponse)
