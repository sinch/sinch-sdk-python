from sinch.domains.conversation.models.capability.responses import QueryConversationCapabilityResponse


def test_capability_query(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    query_capability_response = sinch_client_sync.conversation.capability.query(
        app_id=app_id,
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        }
    )
    assert isinstance(query_capability_response, QueryConversationCapabilityResponse)


async def test_capability_query_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    query_capability_response = await sinch_client_async.conversation.capability.query(
        app_id=app_id,
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        }
    )
    assert isinstance(query_capability_response, QueryConversationCapabilityResponse)
