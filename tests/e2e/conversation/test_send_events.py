from sinch.domains.conversation.models.event.responses import SendConversationEventResponse


def test_send_event(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    send_event_response = sinch_client_sync.conversation.event.send(
        app_id=app_id,
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        },
        event={
            "composing_event": {}
        }
    )
    assert isinstance(send_event_response, SendConversationEventResponse)


async def test_send_event_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    send_event_response = await sinch_client_async.conversation.event.send(
        app_id=app_id,
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        },
        event={
            "composing_event": {}
        }
    )
    assert isinstance(send_event_response, SendConversationEventResponse)
