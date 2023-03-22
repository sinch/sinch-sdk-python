from sinch.domains.conversation.models.app.responses import GetConversationAppResponse


def test_get_conversation_app(sinch_client_sync):
    list_apps_response = sinch_client_sync.conversation.app.list()

    get_app_response = sinch_client_sync.conversation.app.get(
        app_id=list_apps_response.apps[0].id
    )
    assert isinstance(get_app_response, GetConversationAppResponse)


async def test_get_conversation_app_async(sinch_client_async, sinch_client_sync):
    list_apps_response = sinch_client_sync.conversation.app.list()

    get_app_response = await sinch_client_async.conversation.app.get(
        app_id=list_apps_response.apps[0].id
    )
    assert isinstance(get_app_response, GetConversationAppResponse)
