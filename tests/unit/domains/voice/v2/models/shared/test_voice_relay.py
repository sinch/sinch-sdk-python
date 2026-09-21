from sinch.domains.voice.models.v2.shared.voice_relay import (
    VoiceRelay,
    VoiceRelayDetails,
)


def test_voice_relay_details_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = VoiceRelayDetails(
        endpoint="wss://acme.com/agent",
        enable_interruptions=True,
        tts_voice="Emma",
        stt_language="en-US",
        call_headers=[{"key": "my-key", "value": "my-key-value"}],
    )

    assert model.endpoint == "wss://acme.com/agent"
    assert model.enable_interruptions is True
    assert model.tts_voice == "Emma"
    assert model.stt_language == "en-US"
    assert model.call_headers[0].key == "my-key"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["enableInterruptions"] is True
    assert alias_dump["ttsVoice"] == "Emma"
    assert alias_dump["sttLanguage"] == "en-US"
    assert alias_dump["callHeaders"] == [
        {"key": "my-key", "value": "my-key-value"}
    ]


def test_voice_relay_details_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = VoiceRelayDetails(
        endpoint="wss://acme.com/agent", tts_voice="Emma", stt_language="en-US"
    )

    assert model.enable_interruptions is None
    assert model.call_headers is None


def test_voice_relay_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = VoiceRelay(
        type="VOICE_RELAY",
        voice_relay={
            "endpoint": "wss://acme.com/agent",
            "tts_voice": "Emma",
            "stt_language": "en-US",
        },
    )

    assert model.type == "VOICE_RELAY"
    assert model.voice_relay.endpoint == "wss://acme.com/agent"
    assert model.voice_relay.tts_voice == "Emma"
    assert model.voice_relay.stt_language == "en-US"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["voiceRelay"]["ttsVoice"] == "Emma"
    assert alias_dump["voiceRelay"]["sttLanguage"] == "en-US"
