from sinch.domains.voice.models.applications.responses import UnassignNumbersVoiceApplicationResponse


def test_unassign_application_number(
    sinch_client_sync
):
    get_voice_numbers_response = sinch_client_sync.voice.applications.get_numbers()
    unassign_number_response = sinch_client_sync.voice.applications.unassign_number(
        number=get_voice_numbers_response.numbers[0].number
    )
    assert isinstance(unassign_number_response, UnassignNumbersVoiceApplicationResponse)


async def test_unassign_application_number_async(
    sinch_client_async
):
    get_voice_numbers_response = await sinch_client_async.voice.applications.get_numbers()
    unassign_number_response = await sinch_client_async.voice.applications.unassign_number(
        number=get_voice_numbers_response.numbers[0].number
    )
    assert isinstance(unassign_number_response, UnassignNumbersVoiceApplicationResponse)
