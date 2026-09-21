import pytest
from pydantic import ValidationError

from sinch.domains.sms.models.v1.internal.group_request import GroupRequest


def test_group_request_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = GroupRequest()

    assert model.name is None
    assert model.members is None
    assert model.child_groups is None
    assert model.auto_update is None


def test_group_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = GroupRequest(
        name="Test Group",
        members=["+46701234567", "+46709876543"],
        child_groups=["01FC66621VHDBN119Z8PMV1AHY"],
        auto_update={
            "to": "+15551231234",
            "add": {"first_word": "JOIN"},
            "remove": {"first_word": "LEAVE"},
        },
    )

    assert model.name == "Test Group"
    assert model.members == ["+46701234567", "+46709876543"]
    assert model.child_groups == ["01FC66621VHDBN119Z8PMV1AHY"]
    assert model.auto_update.to == "+15551231234"
    assert model.auto_update.add.first_word == "JOIN"
    assert model.auto_update.remove.first_word == "LEAVE"


def test_group_request_expects_auto_update_nested_parsing():
    """Test that auto_update parses nested add and remove keywords correctly."""
    model = GroupRequest(
        auto_update={
            "to": "+15551231234",
            "add": {"first_word": "JOIN", "second_word": "NOW"},
            "remove": {"first_word": "LEAVE"},
        }
    )

    assert model.auto_update.to == "+15551231234"
    assert model.auto_update.add.first_word == "JOIN"
    assert model.auto_update.add.second_word == "NOW"
    assert model.auto_update.remove.first_word == "LEAVE"
    assert model.auto_update.remove.second_word is None
