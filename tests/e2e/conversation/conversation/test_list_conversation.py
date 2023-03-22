from sinch.domains.conversation.models.conversation.responses import SinchListConversationsResponse


def test_list_conversation(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_conversations_response = sinch_client_sync.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(list_conversations_response.result, SinchListConversationsResponse)


async def test_list_conversation_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    list_conversations_response = await sinch_client_async.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(list_conversations_response.result, SinchListConversationsResponse)
