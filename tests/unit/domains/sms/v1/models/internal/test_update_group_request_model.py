import pytest
from pydantic import ValidationError

from sinch.domains.sms.models.v1.internal.update_group_request import UpdateGroupRequest


def test_update_group_request_expects_required_group_id():
    """Test that group_id is required."""
    with pytest.raises(ValidationError):
        UpdateGroupRequest()


def test_update_group_request_expects_optional_fields_default_to_none():
    """Test that all optional fields default to None when only group_id is provided."""
    model = UpdateGroupRequest(group_id="01FC66621XXXXX119Z8PMV1QPQ")

    assert model.group_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert model.add is None
    assert model.remove is None
    assert model.name is None
    assert model.add_from_group is None
    assert model.remove_from_group is None
    assert model.auto_update is None


def test_update_group_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = UpdateGroupRequest(
        group_id="01FC66621XXXXX119Z8PMV1QPQ",
        name="Updated Group",
        add=["+46701234567", "+46709876543"],
        remove=["+46701111111"],
        add_from_group="01FC66621VHDBN119Z8PMV1AHY",
        remove_from_group="01FC66621VHDBN119Z8PMV1AHZ",
        auto_update={
            "to": "+15551231234",
            "add": {"first_word": "JOIN"},
            "remove": {"first_word": "LEAVE"},
        },
    )

    assert model.group_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert model.name == "Updated Group"
    assert model.add == ["+46701234567", "+46709876543"]
    assert model.remove == ["+46701111111"]
    assert model.add_from_group == "01FC66621VHDBN119Z8PMV1AHY"
    assert model.remove_from_group == "01FC66621VHDBN119Z8PMV1AHZ"
    assert model.auto_update.to == "+15551231234"
    assert model.auto_update.add.first_word == "JOIN"
    assert model.auto_update.remove.first_word == "LEAVE"

