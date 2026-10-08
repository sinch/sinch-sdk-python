from sinch.domains.voice.helpers.v2.svaml import Calls, Messages

SAY = {"type": "SAY", "say": {"text": "Hello", "voice_name": "Emma"}}


def test_text_expects_all_fields():
    """Test that text builds a SAY message without format."""
    assert Messages.text("Hello", "Emma") == SAY


def test_ssml_expects_ssml_format():
    """Test that ssml builds a SAY message in SSML format."""
    assert Messages.ssml("<speak>Hi</speak>", "Brian") == {
        "type": "SAY",
        "say": {
            "text": "<speak>Hi</speak>",
            "voice_name": "Brian",
            "format": "SSML",
        },
    }


def test_play_expects_all_fields():
    """Test that play builds a PLAY message."""
    assert Messages.play("https://example.com/a.mp3") == {
        "type": "PLAY",
        "play": {"url": "https://example.com/a.mp3"},
    }


def test_start_expects_all_fields():
    """Test that start builds the command with all its fields."""
    command = Messages.start(
        Messages.text("Hello", "Emma"),
        name="greeting",
        on_finish=[Calls.hangup()],
    )

    assert command == {
        "command": "messages",
        "messages_name": "greeting",
        "messages": [SAY],
        "events": {"on_finish": [{"command": "hangup"}]},
    }


def test_start_expects_optionals_omitted_when_not_provided():
    """Test that omitted optionals, including events, are not included."""
    assert Messages.start(SAY) == {"command": "messages", "messages": [SAY]}


def test_start_expects_messages_in_order():
    """Test that several messages are kept in the given order."""
    play = Messages.play("https://example.com/a.mp3")
    assert Messages.start(SAY, play)["messages"] == [SAY, play]


def test_start_expects_empty_handler_kept():
    """Test that an explicit empty handler list is kept, so events is sent."""
    assert Messages.start(SAY, on_finish=[])["events"] == {"on_finish": []}


def test_stop_expects_all_fields():
    """Test that stop builds the command with all its fields."""
    assert Messages.stop("greeting") == {
        "command": "stopMessages",
        "messages_name": "greeting",
    }
