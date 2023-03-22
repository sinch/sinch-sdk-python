from sinch.domains.conversation.models.conversation.responses import SinchUpdateConversationResponse


def test_update_conversation(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_conversations_response = sinch_client_sync.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )

    update_conversation_response = sinch_client_sync.conversation.conversation.update(
        active=False,
        conversation_id=list_conversations_response.result.conversations[0].id
    )
    assert isinstance(update_conversation_response, SinchUpdateConversationResponse)


async def test_update_conversation_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    list_conversations_response = await sinch_client_async.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )

    update_conversation_response = await sinch_client_async.conversation.conversation.update(
        active=False,
        conversation_id=list_conversations_response.result.conversations[0].id
    )
    assert isinstance(update_conversation_response, SinchUpdateConversationResponse)
