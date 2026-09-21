from sinch.domains.voice.models.v2.svaml.internal.request.validate_svaml_request import (
    ValidateSvamlRequest,
)


def test_validate_svaml_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ValidateSvamlRequest(
        svaml={"commands": [{"command": "answer"}]},
        validation_type="STRICT",
    )

    assert model.svaml.commands[0].command == "answer"
    assert model.validation_type == "STRICT"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["svaml"]["commands"][0]["command"] == "answer"
    assert alias_dump["validationType"] == "STRICT"


def test_validate_svaml_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ValidateSvamlRequest(svaml={"commands": [{"command": "answer"}]})

    assert model.validation_type is None
