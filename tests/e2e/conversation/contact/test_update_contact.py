from sinch.domains.conversation.models.contact.responses import (
    UpdateConversationContactResponse,
    ListConversationContactsResponse
)


def test_update_sms_contact(sinch_client_sync, phone_number):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    update_contact_response = sinch_client_sync.conversation.contact.update(
        contact_id=list_contacts_response.result.contacts[0].id,
        email="tytusb@sample.pl",
        display_name="Tytus Bomba",
        language="PL"
    )
    assert isinstance(update_contact_response, UpdateConversationContactResponse)
    assert update_contact_response.email != list_contacts_response.result.contacts[0].email


async def test_update_sms_contact_async(sinch_client_async, phone_number):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    assert isinstance(list_contacts_response.result, ListConversationContactsResponse)

    update_contact_response = await sinch_client_async.conversation.contact.update(
        contact_id=list_contacts_response.result.contacts[0].id,
        email="tytusb@sample.pl",
        display_name="Tytus Bomba",
        language="PL"
    )
    assert isinstance(update_contact_response, UpdateConversationContactResponse)
    assert update_contact_response.email != list_contacts_response.result.contacts[0].email
