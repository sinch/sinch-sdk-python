from sinch.domains.conversation.models.webhook.responses import SinchListWebhooksResponse


def test_list_webhook(sinch_client_sync, app_id):
    list_webhook_response = sinch_client_sync.conversation.webhook.list(
        app_id=app_id,
    )
    assert isinstance(list_webhook_response, SinchListWebhooksResponse)


async def test_list_webhook_async(sinch_client_async, app_id):
    list_webhook_response = await sinch_client_async.conversation.webhook.list(
        app_id=app_id,
    )
    assert isinstance(list_webhook_response, SinchListWebhooksResponse)
