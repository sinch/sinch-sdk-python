from sinch.domains.conversation.models.contact.responses import CreateConversationContactResponse
from sinch.domains.conversation.enums import ConversationChannel


def test_create_sms_contact(sinch_client_sync, phone_number):
    sms_contact_response = sinch_client_sync.conversation.contact.create(
        channel_identities=[
            {
                "channel": ConversationChannel.SMS.value,
                "identity": "12345673932"
            }
        ],
        language="PL",
        display_name="Guido van Rossum",
        email="sample@email.com",
        metadata="test"
    )
    assert isinstance(sms_contact_response, CreateConversationContactResponse)
    assert sms_contact_response.display_name == "Guido van Rossum"


def test_create_messanger_contact(sinch_client_sync, phone_number):
    list_apps_response = sinch_client_sync.conversation.app.list()
    messanger_contact_response = sinch_client_sync.conversation.contact.create(
        channel_identities=[
            {
                "channel": ConversationChannel.MESSENGER.value,
                "identity": "Sebastian4",
                "app_id": list_apps_response.apps[0].id
            }
        ],
        language="PL",
        display_name="Sebastian",
        email="sebastian@email.com",
        metadata="test"
    )
    assert isinstance(messanger_contact_response, CreateConversationContactResponse)
    assert messanger_contact_response.display_name == "Sebastian"


async def test_create_sms_contact_async(sinch_client_async, phone_number):
    sms_contact_response = await sinch_client_async.conversation.contact.create(
        channel_identities=[
            {
                "channel": ConversationChannel.SMS.value,
                "identity": "12345673932"
            }
        ],
        language="PL",
        display_name="Guido van Rossum",
        email="sample@email.com",
        metadata="test"
    )
    assert isinstance(sms_contact_response, CreateConversationContactResponse)
    assert sms_contact_response.display_name == "Guido van Rossum"
