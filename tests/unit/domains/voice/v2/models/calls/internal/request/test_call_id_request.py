from sinch.domains.voice.models.v2.calls.internal.request.call_id_request import (
    CallIdRequest,
)


def test_call_id_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CallIdRequest(call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA")

    assert model.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["callId"] == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
