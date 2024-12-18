from sinch.domains.conversation.models.contact.responses import (
    MergeConversationContactsResponse,
    ListConversationContactsResponse
)


def test_merge_contacts(sinch_client_sync):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    merge_contacts_response = sinch_client_sync.conversation.contact.merge(
        source_id=list_contacts_response.result.contacts[1].id,
        destination_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(merge_contacts_response, MergeConversationContactsResponse)


async def test_merge_contacts_async(sinch_client_async):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    merge_contacts_response = await sinch_client_async.conversation.contact.merge(
        source_id=list_contacts_response.result.contacts[1].id,
        destination_id=list_contacts_response.result.contacts[0].id
    )
    assert isinstance(merge_contacts_response, MergeConversationContactsResponse)
