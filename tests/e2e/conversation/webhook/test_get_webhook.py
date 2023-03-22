from sinch.domains.conversation.models.webhook.responses import GetWebhookResponse


def test_get_webhook(sinch_client_sync, app_id):
    list_webhook_response = sinch_client_sync.conversation.webhook.list(
        app_id=app_id
    )
    get_webhook_response = sinch_client_sync.conversation.webhook.get(
        webhook_id=list_webhook_response.webhooks[1].id
    )
    assert isinstance(get_webhook_response, GetWebhookResponse)


async def test_get_webhook_async(sinch_client_async, app_id):
    list_webhook_response = await sinch_client_async.conversation.webhook.list(
        app_id=app_id
    )
    get_webhook_response = await sinch_client_async.conversation.webhook.get(
        webhook_id=list_webhook_response.webhooks[1].id
    )
    assert isinstance(get_webhook_response, GetWebhookResponse)
