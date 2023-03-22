import pytest
from sinch.domains.conversation.models.conversation.responses import SinchInjectMessageResponse


@pytest.mark.skip(reason="More advanced testing setup required.")  # TODO: fix that
def test_inject_message_to_conversation(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_conversations_response = sinch_client_sync.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )
    inject_message_response = sinch_client_sync.conversation.conversation.inject_message_to_conversation(
        conversation_id=list_conversations_response.result.conversations[0].id,
        direction="TO_APP",
        contact_message={},
        channel_identity={}
    )
    assert isinstance(inject_message_response, SinchInjectMessageResponse)


@pytest.mark.skip(reason="More advanced testing setup required.")  # TODO: fix that
async def test_inject_message_to_conversation_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    list_conversations_response = await sinch_client_async.conversation.conversation.list(
        only_active=False,
        contact_id=list_contacts_response.result.contacts[0].id
    )
    stop_conversation_response = await sinch_client_async.conversation.conversation.inject_message_to_conversation(
        conversation_id=list_conversations_response.result.conversations[0].id,
        direction="TO_APP",
        contact_message={},
        channel_identity={}
    )
    assert isinstance(stop_conversation_response, SinchInjectMessageResponse)
