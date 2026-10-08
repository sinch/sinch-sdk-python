from sinch.domains.voice.helpers.v2.svaml import Amd, Calls


def test_activate_expects_all_fields():
    """Test that activate builds the command with all its fields."""
    command = Amd.activate(
        on_human=[Calls.bridge_call("my-bridge")],
        on_machine=[Calls.hangup()],
        on_beep=[Calls.pause(1000)],
        on_unknown=[Calls.hangup()],
    )

    assert command == {
        "command": "amd",
        "events": {
            "on_human": [
                {"command": "bridgeCall", "bridge_name": "my-bridge"}
            ],
            "on_machine": [{"command": "hangup"}],
            "on_beep": [{"command": "pause", "duration_milliseconds": 1000}],
            "on_unknown": [{"command": "hangup"}],
        },
    }


def test_activate_expects_events_omitted_when_not_provided():
    """Test that events is not included when no handler is provided."""
    assert Amd.activate() == {"command": "amd"}


def test_activate_expects_empty_handler_kept():
    """Test that an explicit empty handler list is kept, so events is sent."""
    assert Amd.activate(on_beep=[])["events"] == {"on_beep": []}


def test_activate_expects_single_command_handler_wrapped():
    """Test that a handler given as a single command is sent as a list."""
    command = Amd.activate(on_machine=Calls.hangup())
    assert command["events"] == {"on_machine": [{"command": "hangup"}]}
