from sinch.domains.conversation.models.app.responses import ListConversationAppsResponse


def test_list_conversation_apps(sinch_client_sync):
    list_apps_response = sinch_client_sync.conversation.app.list()
    assert isinstance(list_apps_response, ListConversationAppsResponse)


async def test_list_conversation_apps_async(sinch_client_async):
    list_apps_response = await sinch_client_async.conversation.app.list()
    assert isinstance(list_apps_response, ListConversationAppsResponse)


async def test_list_conversation_apps_empty_response_async(sinch_client_async, empty_project_id):
    sinch_client_async.configuration.project_id = empty_project_id
    list_apps_response = await sinch_client_async.conversation.app.list()
    assert isinstance(list_apps_response, ListConversationAppsResponse)
    assert len(list_apps_response.apps) == 0
