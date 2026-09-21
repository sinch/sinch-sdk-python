from sinch.domains.voice.models.v2.batches.response.batch_stop_response import (
    BatchStopResponse,
)


def test_batch_stop_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = BatchStopResponse(result="STOP_REQUESTED")

    assert model.result == "STOP_REQUESTED"

    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["result"] == "STOP_REQUESTED"


def test_batch_stop_response_expects_result_defaults_to_none():
    """Test that the optional result field defaults to None."""
    model = BatchStopResponse()

    assert model.result is None
