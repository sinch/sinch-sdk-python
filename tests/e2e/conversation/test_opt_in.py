from sinch.domains.conversation.models.opt_in_opt_out.responses import RegisterConversationOptInResponse


def test_register_opt_in(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    opt_in_response = sinch_client_sync.conversation.opt_in.register(
        app_id=app_id,
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        },
        channels=["WHATSAPP"]
    )
    assert isinstance(opt_in_response, RegisterConversationOptInResponse)


async def test_register_opt_in_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    opt_in_response = await sinch_client_async.conversation.opt_in.register(
        app_id=app_id,
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        },
        channels=["WHATSAPP"]
    )
    assert isinstance(opt_in_response, RegisterConversationOptInResponse)
