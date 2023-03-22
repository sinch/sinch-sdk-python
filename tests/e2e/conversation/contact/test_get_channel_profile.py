import pytest

from sinch.domains.conversation.models.contact.responses import (
    GetConversationChannelProfileResponse,
    ListConversationContactsResponse
)


@pytest.mark.skip(reason="More advanced testing setup required.")  # TODO: fix that
def test_get_channel_profile(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    list_apps_response = sinch_client_sync.conversation.app.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    get_profile_response = sinch_client_sync.conversation.contact.get_channel_profile(
        channel="MESSENGER",
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        },
        app_id=list_apps_response.apps[0].id
    )
    assert isinstance(get_profile_response.result, GetConversationChannelProfileResponse)


@pytest.mark.skip(reason="More advanced testing setup required.")  # TODO: fix that
async def test_get_channel_profile_async(sinch_client_async):
    list_apps_response = await sinch_client_async.conversation.app.list()
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    get_profile_response = await sinch_client_async.conversation.contact.get_channel_profile(
        channel="MESSENGER",
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        },
        app_id=list_apps_response.apps[0].id
    )
    assert isinstance(get_profile_response.result, GetConversationChannelProfileResponse)
