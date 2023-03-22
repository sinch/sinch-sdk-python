from sinch.domains.conversation.models.templates.responses import GetConversationTemplateResponse


def test_get_template(sinch_client_sync):
    list_template_response = sinch_client_sync.conversation.template.list()
    get_template_response = sinch_client_sync.conversation.template.get(
        template_id=list_template_response.templates[0].id
    )
    assert isinstance(get_template_response, GetConversationTemplateResponse)


def test_get_template_async(sinch_client_sync):
    list_template_response = sinch_client_sync.conversation.template.list()
    get_template_response = sinch_client_sync.conversation.template.get(
        template_id=list_template_response.templates[0].id
    )
    assert isinstance(get_template_response, GetConversationTemplateResponse)
