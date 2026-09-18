from sinch.domains.voice.models.v2.svaml.internal.request.describe_svaml_request import (
    DescribeSvamlRequest,
)


def test_describe_svaml_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DescribeSvamlRequest(svaml={"commands": [{"command": "answer"}]})

    assert model.svaml.commands[0].command == "answer"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["svaml"]["commands"][0]["command"] == "answer"
