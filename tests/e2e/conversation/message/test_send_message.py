from sinch.domains.conversation.models.message.responses import SendConversationMessageResponse


def test_send_message_messenger_contact(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    send_message_response = sinch_client_sync.conversation.message.send(
        app_id=app_id,
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        },
        message={
            "text_message": {
                "text": "Kluski, rolada i modro kapusta."
            }
        }
    )
    assert isinstance(send_message_response, SendConversationMessageResponse)


async def test_send_message_messenger_contact_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    send_message_response = await sinch_client_async.conversation.message.send(
        app_id=app_id,
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        },
        message={
            "text_message": {
                "text": "Kluski, rolada i modro kapusta."
            }
        }
    )
    assert isinstance(send_message_response, SendConversationMessageResponse)
