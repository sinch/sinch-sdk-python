from sinch.domains.voice.models.applications.responses import GetNumbersVoiceApplicationResponse


def test_get_application_numbers(
    sinch_client_sync
):
    get_voice_numbers_response = sinch_client_sync.voice.applications.get_numbers()
    assert isinstance(get_voice_numbers_response, GetNumbersVoiceApplicationResponse)


async def test_get_application_numbers_async(
    sinch_client_async
):
    get_voice_numbers_response = await sinch_client_async.voice.applications.get_numbers()
    assert isinstance(get_voice_numbers_response, GetNumbersVoiceApplicationResponse)
