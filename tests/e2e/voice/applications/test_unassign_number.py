from sinch.domains.voice.models.applications.responses import UnassignNumbersVoiceApplicationResponse


def test_unassign_application_number(
    sinch_client_sync
):
    unassign_number_response = sinch_client_sync.voice.applications.get_callback_urls()
    assert isinstance(unassign_number_response, UnassignNumbersVoiceApplicationResponse)
