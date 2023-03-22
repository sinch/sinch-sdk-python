from sinch.domains.conversation.models.opt_in_opt_out.responses import RegisterConversationOptOutResponse


def test_register_opt_out(sinch_client_sync, app_id):
    list_contacts_response = sinch_client_sync.conversation.contact.list()
    opt_out_response = sinch_client_sync.conversation.opt_out.register(
        app_id=app_id,
        recipient={
            "contact_id": list_contacts_response.result.contacts[0].id
        },
        channels=["WHATSAPP"]
    )
    assert isinstance(opt_out_response, RegisterConversationOptOutResponse)


async def test_register_opt_out_async(sinch_client_async, app_id):
    list_contacts_response = await sinch_client_async.conversation.contact.list()
    opt_out_response = await sinch_client_async.conversation.opt_out.register(
        app_id=app_id,
        recipient={

            "contact_id": list_contacts_response.result.contacts[0].id
        },
        channels=["WHATSAPP"]
    )
    assert isinstance(opt_out_response, RegisterConversationOptOutResponse)
