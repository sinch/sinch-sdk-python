from sinch.domains.voice.helpers.v2.svaml import Calls, Recording

URL = "s3://bucket/calls"
CREDENTIALS = "key:secret:eu-central-1"


def test_options_expects_required_fields_only():
    """Test that omitted optionals are not included."""
    assert Recording.options("GCP", URL, CREDENTIALS) == {
        "destination": "GCP",
        "destination_url": URL,
        "credentials": CREDENTIALS,
    }


def test_options_expects_all_fields():
    """Test that the options include all the optional fields."""
    assert Recording.options(
        "AWS",
        URL,
        CREDENTIALS,
        format="WAV",
        recording_type="INBOUND",
        transcription_options={"is_enabled": True, "locale": "es-ES"},
    ) == {
        "destination": "AWS",
        "destination_url": URL,
        "credentials": CREDENTIALS,
        "format": "WAV",
        "recording_type": "INBOUND",
        "transcription_options": {"is_enabled": True, "locale": "es-ES"},
    }


def test_start_expects_all_fields():
    """Test that start builds the command with all its fields."""
    options = Recording.options("AWS", URL, CREDENTIALS)
    command = Recording.start(
        options,
        name="rec",
        on_finish=[Calls.hangup()],
        on_failure=[Calls.hangup()],
    )

    assert command == {
        "command": "startRecording",
        "recording_name": "rec",
        "recording_options": options,
        "events": {
            "on_finish": [{"command": "hangup"}],
            "on_failure": [{"command": "hangup"}],
        },
    }


def test_start_expects_optionals_omitted_when_not_provided():
    """Test that omitted optionals, including events, are not included."""
    options = Recording.options("GCP", URL, CREDENTIALS)
    assert Recording.start(options) == {
        "command": "startRecording",
        "recording_options": options,
    }


def test_start_expects_empty_handler_kept():
    """Test that an explicit empty handler list is kept, so events is sent."""
    command = Recording.start(
        Recording.options("AWS", URL, CREDENTIALS), on_failure=[]
    )
    assert command["events"] == {"on_failure": []}


def test_stop_expects_all_fields():
    """Test that stop builds the command with all its fields."""
    assert Recording.stop("rec") == {
        "command": "stopRecording",
        "recording_name": "rec",
    }
