from sinch.domains.voice.models.callouts.responses import CalloutResponse


def test_tts_callout(
    sinch_client_sync,
    phone_number,
    origin_phone_number
):
    tts_callout_response = sinch_client_sync.voice.callouts.text_to_speech(
        destination={
            "type": "number",
            "endpoint": phone_number
        },
        text="test message",
        locale="en-US",
        cli=origin_phone_number
    )
    assert isinstance(tts_callout_response, CalloutResponse)


def test_custom_callout(
    sinch_client_sync,
    phone_number,
    origin_phone_number
):
    custom_callout_response = sinch_client_sync.voice.callouts.conference(
        destination={
            "type": "number",
            "endpoint": phone_number
        },
        text="test message",
        locale="en-US",
        cli=origin_phone_number
    )
    assert isinstance(custom_callout_response, CalloutResponse)


def test_conference_callout(
    sinch_client_sync,
    phone_number,
    origin_phone_number
):
    conference_callout_response = sinch_client_sync.callouts.custom(
        destination={
            "type": "number",
            "endpoint": phone_number
        },
        text="test message",
        locale="en-US",
        cli=origin_phone_number
    )
    assert isinstance(conference_callout_response, CalloutResponse)
