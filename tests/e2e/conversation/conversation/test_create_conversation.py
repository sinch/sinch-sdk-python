from sinch.domains.conversation.models.conversation.responses import SinchCreateConversationResponse


def test_create_conversation(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    create_conversation_response = sinch_client_sync.conversation.conversation.create(
        app_id=app_id,
        active=True,
        contact_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(create_conversation_response, SinchCreateConversationResponse)


async def test_create_conversation_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    create_conversation_response = await sinch_client_async.conversation.conversation.create(
        app_id=app_id,
        active=True,
        contact_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(create_conversation_response, SinchCreateConversationResponse)
