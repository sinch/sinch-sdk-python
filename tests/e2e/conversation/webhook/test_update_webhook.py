from sinch.domains.conversation.models.webhook.responses import UpdateWebhookResponse


def test_update_webhook(sinch_client_sync, app_id):
    list_webhook_response = sinch_client_sync.conversation.webhook.list(
        app_id=app_id
    )
    update_webhook_response = sinch_client_sync.conversation.webhook.update(
        app_id=app_id,
        webhook_id=list_webhook_response.webhooks[1].id,
        target="http://import.antigravity3.pl",
        triggers=["MESSAGE_DELIVERY", "CONTACT_MERGE"]
    )
    assert isinstance(update_webhook_response, UpdateWebhookResponse)


async def test_update_webhook_async(sinch_client_async, app_id):
    list_webhook_response = await sinch_client_async.conversation.webhook.list(
        app_id=app_id
    )
    update_webhook_response = await sinch_client_async.conversation.webhook.update(
        app_id=app_id,
        webhook_id=list_webhook_response.webhooks[1].id,
        target="http://import.antigravity3.pl",
        triggers=["MESSAGE_DELIVERY", "CONTACT_MERGE"]
    )
    assert isinstance(update_webhook_response, UpdateWebhookResponse)
