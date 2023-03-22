from sinch.domains.conversation.models.webhook.responses import CreateWebhookResponse


def test_create_webhook(sinch_client_sync, app_id):
    create_webhook_response = sinch_client_sync.conversation.webhook.create(
        app_id=app_id,
        target="http://import.antigravity8.pl",
        triggers=["MESSAGE_DELIVERY", "CONTACT_MERGE"]
    )
    assert isinstance(create_webhook_response, CreateWebhookResponse)


async def test_create_webhook_async(sinch_client_async, app_id):
    create_webhook_response = await sinch_client_async.conversation.webhook.create(
        app_id=app_id,
        target="http://import.antigravity8.pl",
        triggers=["MESSAGE_DELIVERY", "CONTACT_MERGE"]
    )
    assert isinstance(create_webhook_response, CreateWebhookResponse)
