from sinch.domains.conversation.models.conversation.responses import SinchStopConversationResponse


def test_stop_conversation_sync(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_conversations_response = sinch_client_sync.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )
    stop_conversation_response = sinch_client_sync.conversation.conversation.stop(
        conversation_id=list_conversations_response.result.conversations[1].id
    )
    assert isinstance(stop_conversation_response, SinchStopConversationResponse)


async def test_stop_conversation_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    list_conversations_response = await sinch_client_async.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )
    stop_conversation_response = await sinch_client_async.conversation.conversation.stop(
        conversation_id=list_conversations_response.result.conversations[1].id
    )
    assert isinstance(stop_conversation_response, SinchStopConversationResponse)
