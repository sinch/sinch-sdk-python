from sinch.domains.voice.models.v2.batches.internal.request.batch_id_request import (
    BatchIdRequest,
)


def test_batch_id_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = BatchIdRequest(batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC")

    assert model.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"


    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["batchId"] == "01BX5ZZKBKACTAV9WEVGEMMVRC"