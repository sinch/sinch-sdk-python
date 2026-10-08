from sinch.domains.voice.helpers.v2.svaml import Calls

TO = {"type": "PHONE", "phone": {"number": "+15559876543"}}
FROM = {"type": "PHONE", "phone": {"number": "+15551234567"}}


def test_answer_expects_answer_command():
    """Test that answer builds the command."""
    assert Calls.answer() == {"command": "answer"}


def test_bridge_call_expects_all_fields():
    """Test that bridge_call builds the command with all its fields."""
    assert Calls.bridge_call("my-bridge") == {
        "command": "bridgeCall",
        "bridge_name": "my-bridge",
    }


def test_dial_expects_all_fields():
    """Test that dial builds the command with all its fields."""
    command = Calls.dial(
        TO,
        from_=FROM,
        name="origin",
        timeout_duration_seconds=30,
        max_duration_seconds=3600,
        on_answer=[Calls.answer()],
        on_busy=[Calls.hangup()],
        on_reject=[Calls.hangup()],
        on_timeout=[Calls.hangup()],
        on_hangup=[Calls.hangup("destination")],
        on_failure=[Calls.hangup()],
    )

    assert command == {
        "command": "dial",
        "to": TO,
        "from_": FROM,
        "call_name": "origin",
        "dial_timeout_duration_seconds": 30,
        "max_call_duration_seconds": 3600,
        "events": {
            "on_answer": [{"command": "answer"}],
            "on_busy": [{"command": "hangup"}],
            "on_reject": [{"command": "hangup"}],
            "on_timeout": [{"command": "hangup"}],
            "on_hangup": [{"command": "hangup", "call_name": "destination"}],
            "on_failure": [{"command": "hangup"}],
        },
    }


def test_dial_expects_optionals_omitted_when_not_provided():
    """Test that omitted optionals, including events, are not included."""
    assert Calls.dial(TO) == {"command": "dial", "to": TO}


def test_dial_expects_empty_handler_kept():
    """Test that an explicit empty handler list is kept, so events is sent."""
    assert Calls.dial(TO, on_answer=[])["events"] == {"on_answer": []}


def test_dial_expects_str_endpoints_as_phone():
    """Test that plain string to and from_ are built as phone endpoints."""
    command = Calls.dial("+15559876543", from_="+15551234567")
    assert command["to"] == TO
    assert command["from_"] == FROM


def test_dial_expects_str_endpoints_parsed_by_prefix():
    """Test that string to and from_ are parsed with Destination.of."""
    command = Calls.dial("sip:bob@example.com", from_="sip:alice@example.com")
    assert command["to"] == {
        "type": "SIP",
        "sip": {"endpoint": "sip:bob@example.com"},
    }
    assert command["from_"] == {
        "type": "SIP",
        "sip": {"endpoint": "sip:alice@example.com"},
    }


def test_hangup_expects_all_fields():
    """Test that hangup builds the command with all its fields."""
    assert Calls.hangup("origin") == {
        "command": "hangup",
        "call_name": "origin",
    }


def test_pause_expects_all_fields():
    """Test that pause builds the command with all its fields."""
    assert Calls.pause(1500) == {
        "command": "pause",
        "duration_milliseconds": 1500,
    }
