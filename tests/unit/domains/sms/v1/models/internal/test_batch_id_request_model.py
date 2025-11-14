import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.internal import BatchIdRequest


def test_batch_id_request_expects_valid_batch_id():
    """Test that the model correctly parses a valid batch_id."""
    batch_id = "01FC66621XXXXX119Z8PMV1QPQ"
    request = BatchIdRequest(batch_id=batch_id)

    assert request.batch_id == batch_id


def test_batch_id_request_expects_batch_id_as_string():
    """Test that batch_id must be a string."""
    with pytest.raises(ValidationError):
        BatchIdRequest(batch_id=12345)

    with pytest.raises(ValidationError):
        BatchIdRequest(batch_id=None)


def test_batch_id_request_expects_model_dump():
    """Test that model_dump correctly serializes the request."""
    batch_id = "01W4FFL35P4NC4K35SMSBATCH1"
    request = BatchIdRequest(batch_id=batch_id)

    dumped = request.model_dump(by_alias=True)
    # batch_id field doesn't have an alias, so it stays as snake_case
    assert dumped["batch_id"] == batch_id

    dumped_no_alias = request.model_dump(by_alias=False)
    assert dumped_no_alias["batch_id"] == batch_id
