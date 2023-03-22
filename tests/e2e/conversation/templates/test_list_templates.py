from sinch.domains.conversation.models.templates.responses import ListConversationTemplatesResponse


def test_list_templates(sinch_client_sync):
    list_template_response = sinch_client_sync.conversation.template.list()
    assert isinstance(list_template_response, ListConversationTemplatesResponse)


async def test_list_templates_async(sinch_client_async):
    list_template_response = await sinch_client_async.conversation.template.list()
    assert isinstance(list_template_response, ListConversationTemplatesResponse)
