from sinch.domains.voice.models.v2.svaml.response.describe_svaml_response import (
    DescribeSvamlResponse,
)


def test_describe_svaml_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DescribeSvamlResponse(
        description="The call is answered and a TTS message is played using the voice Emma."
    )

    assert model.description == (
        "The call is answered and a TTS message is played using the voice Emma."
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["description"] == (
        "The call is answered and a TTS message is played using the voice Emma."
    )


def test_svaml_description_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = DescribeSvamlResponse()

    assert model.description is None
