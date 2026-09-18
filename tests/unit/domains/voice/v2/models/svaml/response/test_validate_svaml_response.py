from sinch.domains.voice.models.v2.svaml.response.validate_svaml_response import (
    ValidateSvamlResponse,
)


def test_validate_svaml_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ValidateSvamlResponse(
        isValid=False,
        errors=["Invalid dial command. Missing destination."],
    )

    assert model.is_valid is False
    assert model.errors == ["Invalid dial command. Missing destination."]

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["isValid"] is False
    assert alias_dump["errors"] == [
        "Invalid dial command. Missing destination."
    ]


def test_validate_svaml_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ValidateSvamlResponse(isValid=True)

    assert model.errors is None
