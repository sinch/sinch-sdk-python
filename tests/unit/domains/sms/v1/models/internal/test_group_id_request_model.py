import pytest
from pydantic import ValidationError

from sinch.domains.sms.models.v1.internal.group_id_request import GroupIdRequest


def test_group_id_request_expects_valid_group_id():
    """Test that the model correctly parses a valid group_id."""
    request = GroupIdRequest(group_id="01FC66621XXXXX119Z8PMV1QPQ")

    assert request.group_id == "01FC66621XXXXX119Z8PMV1QPQ"


def test_group_id_request_expects_group_id_as_string():
    """Test that group_id must be a string."""
    with pytest.raises(ValidationError):
        GroupIdRequest(group_id=12345)

    with pytest.raises(ValidationError):
        GroupIdRequest(group_id=None)


def test_group_id_request_expects_model_dump():
    """Test that model_dump correctly serializes the request."""
    request = GroupIdRequest(group_id="01FC66621XXXXX119Z8PMV1QPQ")

    dumped = request.model_dump(by_alias=True)
    assert dumped["group_id"] == "01FC66621XXXXX119Z8PMV1QPQ"

    dumped_no_alias = request.model_dump(by_alias=False)
    assert dumped_no_alias["group_id"] == "01FC66621XXXXX119Z8PMV1QPQ"
