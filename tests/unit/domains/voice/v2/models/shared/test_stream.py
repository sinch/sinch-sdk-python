from sinch.domains.voice.models.v2.shared.stream import (
    Stream,
    StreamDetails,
    StreamOptions,
)


def test_stream_options_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StreamOptions(version=1, codec="PCM", sample_rate=16000)

    assert model.version == 1
    assert model.codec == "PCM"
    assert model.sample_rate == 16000

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["sampleRate"] == 16000


def test_stream_options_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = StreamOptions()

    assert model.version is None
    assert model.codec is None
    assert model.sample_rate is None


def test_stream_details_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StreamDetails(
        endpoint="wss://example.com",
        stream_options={"codec": "PCM", "sample_rate": 8000},
        call_headers=[{"key": "my-key", "value": "my-key-value"}],
    )

    assert model.endpoint == "wss://example.com"
    assert model.stream_options.sample_rate == 8000
    assert model.call_headers[0].key == "my-key"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["streamOptions"]["sampleRate"] == 8000
    assert alias_dump["callHeaders"] == [
        {"key": "my-key", "value": "my-key-value"}
    ]


def test_stream_details_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = StreamDetails(endpoint="wss://example.com")

    assert model.stream_options is None
    assert model.call_headers is None


def test_stream_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = Stream(
        type="STREAM",
        stream={
            "endpoint": "wss://example.com",
            "stream_options": {"sample_rate": 16000},
        },
    )

    assert model.type == "STREAM"
    assert model.stream.endpoint == "wss://example.com"
    assert model.stream.stream_options.sample_rate == 16000

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["stream"]["streamOptions"]["sampleRate"] == 16000
