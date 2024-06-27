from sinch.domains.voice.models.applications.responses import AssignNumbersVoiceApplicationResponse


def test_assign_application_numbers(
    sinch_client_sync
):
    get_voice_numbers_response = sinch_client_sync.voice.applications.get_numbers()
    assign_voice_numbers_response = sinch_client_sync.voice.applications.assign_numbers(
        numbers=[get_voice_numbers_response.numbers[0].number]
    )
    assert isinstance(assign_voice_numbers_response, AssignNumbersVoiceApplicationResponse)


async def test_assign_application_numbers_async(
    sinch_client_async
):
    get_voice_numbers_response = await sinch_client_async.voice.applications.get_numbers()
    assign_voice_numbers_response = await sinch_client_async.voice.applications.assign_numbers(
        numbers=[get_voice_numbers_response.numbers[0].number]
    )
    assert isinstance(assign_voice_numbers_response, AssignNumbersVoiceApplicationResponse)
