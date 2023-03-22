from sinch.domains.conversation.models.templates.responses import CreateConversationTemplateResponse


def test_create_template(sinch_client_sync):
    create_template_response = sinch_client_sync.conversation.template.create(
        channel="SMS",
        description="pigdog",
        default_translation="pl-PL",
        translations=[
            {"language_code": "pl-PL"}
        ]

    )
    assert isinstance(create_template_response, CreateConversationTemplateResponse)


def test_create_empty_template(sinch_client_sync):
    create_template_response = sinch_client_sync.conversation.template.create(
        default_translation="pl-PL",
        translations=[
            {"language_code": "pl-PL"}
        ]
    )
    assert isinstance(create_template_response, CreateConversationTemplateResponse)


async def test_create_template_async(sinch_client_async):
    create_template_response = await sinch_client_async.conversation.template.create(
        channel="SMS",
        description="pigdog",
        default_translation="pl-PL",
        translations=[
            {"language_code": "pl-PL"}
        ]
    )
    assert isinstance(create_template_response, CreateConversationTemplateResponse)
