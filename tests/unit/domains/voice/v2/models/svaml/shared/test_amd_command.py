from sinch.domains.voice.models.v2.svaml.shared.amd_command import AmdCommand


def test_amd_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = AmdCommand(
        command="amd", events={"on_human": [{"command": "answer"}]}
    )

    assert model.command == "amd"
    assert model.events.on_human[0].command == "answer"


def test_amd_command_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = AmdCommand(command="amd")

    assert model.events is None
