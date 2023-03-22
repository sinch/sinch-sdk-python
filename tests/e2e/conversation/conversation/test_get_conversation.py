from sinch.domains.conversation.models.conversation.responses import SinchGetConversationResponse


def test_get_conversation(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_conversations_response = sinch_client_sync.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )

    get_conversation_response = sinch_client_sync.conversation.conversation.get(
        conversation_id=list_conversations_response.result.conversations[0].id
    )
    assert isinstance(get_conversation_response, SinchGetConversationResponse)


async def test_get_conversation_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    list_conversations_response = await sinch_client_async.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )

    get_conversation_response = await sinch_client_async.conversation.conversation.get(
        conversation_id=list_conversations_response.result.conversations[0].id
    )
    assert isinstance(get_conversation_response, SinchGetConversationResponse)
