from sinch.domains.conversation.models.templates.responses import UpdateConversationTemplateResponse


def test_update_template(sinch_client_sync):
    list_template_response = sinch_client_sync.conversation.template.list()
    update_template_response = sinch_client_sync.conversation.template.update(
        template_id=list_template_response.templates[0].id,
        description="KWK_Wójek",
        default_translation="pl-PL",
        translations=[
            {"language_code": "pl-PL"}
        ]
    )
    assert isinstance(update_template_response, UpdateConversationTemplateResponse)


async def test_update_template_async(sinch_client_sync, sinch_client_async):
    list_template_response = sinch_client_sync.conversation.template.list()
    update_template_response = await sinch_client_async.conversation.template.update(
        template_id=list_template_response.templates[0].id,
        description="KWK_Wójek",
        default_translation="pl-PL",
        translations=[
            {"language_code": "pl-PL"}
        ]
    )
    assert isinstance(update_template_response, UpdateConversationTemplateResponse)
