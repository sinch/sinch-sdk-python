from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_error_details import (
    OptErrorDetails,
)


def test_opt_error_details_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = OptErrorDetails(description="Registration rejected by the channel")

    assert model.description == "Registration rejected by the channel"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["description"] == "Registration rejected by the channel"


def test_opt_error_details_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = OptErrorDetails()

    assert model.description is None
