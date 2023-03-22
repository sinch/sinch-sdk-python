from sinch.domains.conversation.models.templates.responses import DeleteConversationTemplateResponse


def test_delete_template(sinch_client_sync):
    list_template_response = sinch_client_sync.conversation.template.list()
    delete_template_response = sinch_client_sync.conversation.template.delete(
        template_id=list_template_response.templates[0].id
    )
    assert isinstance(delete_template_response, DeleteConversationTemplateResponse)


async def test_delete_template_async(sinch_client_async):
    list_template_response = await sinch_client_async.conversation.template.list()
    delete_template_response = await sinch_client_async.conversation.template.delete(
        template_id=list_template_response.templates[0].id
    )
    assert isinstance(delete_template_response, DeleteConversationTemplateResponse)
