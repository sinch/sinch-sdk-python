from sinch.domains.conversation.models.webhook.responses import SinchDeleteWebhookResponse


def test_delete_webhook(sinch_client_sync, app_id):
    list_webhook_response = sinch_client_sync.conversation.webhook.list(
        app_id=app_id
    )
    delete_webhook_response = sinch_client_sync.conversation.webhook.delete(
        webhook_id=list_webhook_response.webhooks[0].id
    )
    assert isinstance(delete_webhook_response, SinchDeleteWebhookResponse)


async def test_delete_webhook_async(sinch_client_async, app_id):
    list_webhook_response = await sinch_client_async.conversation.webhook.list(
        app_id=app_id,
    )
    delete_webhook_response = await sinch_client_async.conversation.webhook.delete(
        webhook_id=list_webhook_response.webhooks[0].id
    )
    assert isinstance(delete_webhook_response, SinchDeleteWebhookResponse)
