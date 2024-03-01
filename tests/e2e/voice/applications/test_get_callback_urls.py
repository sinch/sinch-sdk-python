from sinch.domains.voice.models.applications.responses import GetCallbackUrlsVoiceApplicationResponse


def test_get_application_callback_urls(
    sinch_client_sync,
    application_key
):
    callback_urls_response = sinch_client_sync.voice.applications.get_callback_urls(
        application_key=application_key
    )
    assert isinstance(callback_urls_response, GetCallbackUrlsVoiceApplicationResponse)


async def test_get_application_callback_async(
    sinch_client_sync,
    application_key
):
    callback_urls_response = sinch_client_sync.voice.applications.get_callback_urls(
        application_key=application_key
    )
    assert isinstance(callback_urls_response, GetCallbackUrlsVoiceApplicationResponse)
