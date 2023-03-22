from sinch.domains.conversation.models.app.responses import DeleteConversationAppResponse


def test_delete_conversation_app(sinch_client_sync):
    list_apps_response = sinch_client_sync.conversation.app.list()

    delete_app_response = sinch_client_sync.conversation.app.delete(
        app_id=list_apps_response.apps[0].id
    )
    assert isinstance(delete_app_response, DeleteConversationAppResponse)


async def test_delete_conversation_app_async(sinch_client_async):
    list_apps_response = await sinch_client_async.conversation.app.list()

    delete_app_response = await sinch_client_async.conversation.app.delete(
        app_id=list_apps_response.apps[0].id
    )
    assert isinstance(delete_app_response, DeleteConversationAppResponse)
