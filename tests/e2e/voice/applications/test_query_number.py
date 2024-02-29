from sinch.domains.voice.models.applications.responses import QueryNumberVoiceApplicationResponse


def test_query_application_numbers_call(
    sinch_client_sync
):
    query_voice_numbers_response = sinch_client_sync.voice.applications.query_number()
    assert isinstance(query_voice_numbers_response, QueryNumberVoiceApplicationResponse)
