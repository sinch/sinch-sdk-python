from sinch.domains.voice.models.v2.svaml.shared.svaml_input import SvamlInput


def test_svaml_input_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SvamlInput(commands=[{"command": "hangup"}])

    assert model.commands[0].command == "hangup"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["commands"][0]["command"] == "hangup"
