from sinch.domains.voice.models.applications.responses import GetCallbackUrlsVoiceApplicationResponse


def test_get_application_callback_urls_call(
    sinch_client_sync
):
    callback_urls_response = sinch_client_sync.voice.applications.get_callback_urls()
    assert isinstance(callback_urls_response, GetCallbackUrlsVoiceApplicationResponse)
