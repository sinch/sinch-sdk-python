from sinch.domains.voice.models.callouts.responses import VoiceCalloutResponse


def test_conference_call(
    sinch_client_sync,
    phone_number,
    voice_origin_phone_number,
    conference_id
):
    conference_callout_response = sinch_client_sync.voice.conferences.call(
        conference_id=conference_id,
        destination={
            "type": "number",
            "endpoint": phone_number
        },
        locale="en-US",
        cli=voice_origin_phone_number
    )
    assert isinstance(conference_callout_response, VoiceCalloutResponse)


async def test_conference_call_async(
    sinch_client_async,
    phone_number,
    voice_origin_phone_number,
    conference_id
):
    conference_callout_response = await sinch_client_async.voice.conferences.call(
        conference_id=conference_id,
        destination={
            "type": "number",
            "endpoint": phone_number
        },
        locale="en-US",
        cli=voice_origin_phone_number
    )
    assert isinstance(conference_callout_response, VoiceCalloutResponse)