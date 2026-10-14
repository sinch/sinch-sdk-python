import pytest

from sinch.domains.voice.helpers.v2.destinations import Destination

PHONE = {"type": "PHONE", "phone": {"number": "+15551234567"}}
SIP = {"type": "SIP", "sip": {"endpoint": "sip:user@example.com"}}
STREAM = {"type": "STREAM", "stream": {"endpoint": "wss://example.com/audio"}}


@pytest.mark.parametrize(
    "value, expected",
    [
        ("+15551234567", PHONE),
        ("phone:+15551234567", PHONE),
        ("sip:user@example.com", SIP),
        (
            "sips:user@example.com",
            {"type": "SIP", "sip": {"endpoint": "sips:user@example.com"}},
        ),
        ("stream:wss://example.com/audio", STREAM),
        (
            "tel:+15551234567",
            {"type": "PHONE", "phone": {"number": "tel:+15551234567"}},
        ),
    ],
)
def test_of_expects_type_detected_from_prefix(value, expected):
    """Test that of detects the type from the prefix, phone by default."""
    assert Destination.of(value) == expected


def test_phone_expects_all_fields():
    """Test that phone builds the endpoint with all its fields."""
    assert Destination.phone("+15551234567") == PHONE


def test_sip_expects_all_fields():
    """Test that sip builds the endpoint with all its fields."""
    assert Destination.sip(
        "sip:user@example.com",
        transport="TCP",
        call_headers=[{"key": "X-Id", "value": "1"}],
    ) == {
        "type": "SIP",
        "sip": {
            "endpoint": "sip:user@example.com",
            "transport": "TCP",
            "call_headers": [{"key": "X-Id", "value": "1"}],
        },
    }


def test_sip_from_expects_all_fields():
    """Test that sip_from builds the origin with all its fields."""
    assert Destination.sip_from(
        "sip:user@example.com", display_name="Alice"
    ) == {
        "type": "SIP",
        "sip": {"endpoint": "sip:user@example.com", "display_name": "Alice"},
    }


def test_stream_expects_all_fields():
    """Test that stream builds the endpoint with all its fields."""
    assert Destination.stream(
        "wss://example.com/audio",
        stream_options={"version": 1, "codec": "PCM", "sample_rate": 16000},
        call_headers=[{"key": "X-Id"}],
    ) == {
        "type": "STREAM",
        "stream": {
            "endpoint": "wss://example.com/audio",
            "stream_options": {
                "version": 1,
                "codec": "PCM",
                "sample_rate": 16000,
            },
            "call_headers": [{"key": "X-Id"}],
        },
    }


def test_voice_relay_expects_all_fields():
    """Test that voice_relay builds the endpoint with all its fields."""
    assert Destination.voice_relay(
        "wss://example.com/agent",
        "en-US-Emma",
        "en-US",
        enable_interruptions=True,
        call_headers=[{"key": "X-Id", "value": "1"}],
    ) == {
        "type": "VOICE_RELAY",
        "voice_relay": {
            "endpoint": "wss://example.com/agent",
            "tts_voice": "en-US-Emma",
            "stt_language": "en-US",
            "enable_interruptions": True,
            "call_headers": [{"key": "X-Id", "value": "1"}],
        },
    }


def test_optionals_expects_omitted_when_not_provided():
    """Test that omitted optionals are not included."""
    assert Destination.sip("sip:user@example.com") == SIP
