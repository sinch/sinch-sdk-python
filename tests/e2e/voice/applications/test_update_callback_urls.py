from sinch.domains.voice.models.applications.responses import UpdateCallbackUrlsVoiceApplicationResponse


def test_update_application_callback_urls(
    sinch_client_sync,
    application_key
):
    callback_urls_response = sinch_client_sync.voice.applications.update_callback_urls(
        application_key=application_key,
        primary="testprimary.com/123",
        fallback="testfallback.com/123"
    )
    assert isinstance(callback_urls_response, UpdateCallbackUrlsVoiceApplicationResponse)


async def test_update_application_callback_urls_async(
    sinch_client_async,
    application_key
):
    callback_urls_response = await sinch_client_async.voice.applications.update_callback_urls(
        application_key=application_key,
        primary="testprimary.com/123",
        fallback="testfallback.com/123"
    )
    assert isinstance(callback_urls_response, UpdateCallbackUrlsVoiceApplicationResponse)
