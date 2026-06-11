import pytest
from pydantic import ValidationError

from sinch.domains.sms.models.v1.internal.replace_group_request import ReplaceGroupRequest


def test_replace_group_request_expects_required_group_id():
    """Test that group_id is required."""
    with pytest.raises(ValidationError):
        ReplaceGroupRequest()


def test_replace_group_request_expects_optional_fields_default_to_none():
    """Test that all optional fields default to None when only group_id is provided."""
    model = ReplaceGroupRequest(group_id="01FC66621XXXXX119Z8PMV1QPQ")

    assert model.group_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert model.name is None
    assert model.members is None
    assert model.child_groups is None
    assert model.auto_update is None


def test_replace_group_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ReplaceGroupRequest(
        group_id="01FC66621XXXXX119Z8PMV1QPQ",
        name="Replaced Group",
        members=["+46701234567", "+46709876543"],
        child_groups=["01FC66621VHDBN119Z8PMV1AHY"],
        auto_update={
            "to": "+15551231234",
            "add": {"first_word": "JOIN"},
            "remove": {"first_word": "LEAVE"},
        },
    )

    assert model.group_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert model.name == "Replaced Group"
    assert model.members == ["+46701234567", "+46709876543"]
    assert model.child_groups == ["01FC66621VHDBN119Z8PMV1AHY"]
    assert model.auto_update.to == "+15551231234"
    assert model.auto_update.add.first_word == "JOIN"
    assert model.auto_update.remove.first_word == "LEAVE"


def test_replace_group_request_expects_group_id_as_string():
    """Test that group_id must be a string."""
    with pytest.raises(ValidationError):
        ReplaceGroupRequest(group_id=123)
