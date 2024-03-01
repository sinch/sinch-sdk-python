from sinch.domains.voice.models.applications.responses import QueryNumberVoiceApplicationResponse


def test_query_application_numbers(
    sinch_client_sync
):
    get_voice_numbers_response = sinch_client_sync.voice.applications.get_numbers()
    query_voice_numbers_response = sinch_client_sync.voice.applications.query_number(
        get_voice_numbers_response.numbers[0].number
    )
    assert isinstance(query_voice_numbers_response, QueryNumberVoiceApplicationResponse)


async def test_query_application_numbers_async(
    sinch_client_async
):
    get_voice_numbers_response = await sinch_client_async.voice.applications.get_numbers()
    query_voice_numbers_response = await sinch_client_async.voice.applications.query_number(
        get_voice_numbers_response.numbers[0].number
    )
    assert isinstance(query_voice_numbers_response, QueryNumberVoiceApplicationResponse)
