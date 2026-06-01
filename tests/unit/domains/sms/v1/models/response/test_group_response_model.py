from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.sms.models.v1.response.group_response import GroupResponse


def test_group_response_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = GroupResponse()

    assert model.id is None
    assert model.name is None
    assert model.size is None
    assert model.created_at is None
    assert model.modified_at is None
    assert model.child_groups is None
    assert model.auto_update is None


def test_group_response_expects_valid_input():
    """Test that the model correctly parses a full valid input."""
    model = GroupResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        name="Test Group",
        size=2,
        created_at="2024-06-06T09:22:14.304Z",
        modified_at="2024-06-06T09:22:48.054Z",
        child_groups=["01FC66621VHDBN119Z8PMV1AHY"],
        auto_update={
            "to": "+15551231234",
            "add": {"first_word": "JOIN"},
            "remove": {"first_word": "LEAVE"},
        },
    )

    assert model.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert model.name == "Test Group"
    assert model.size == 2
    assert model.child_groups == ["01FC66621VHDBN119Z8PMV1AHY"]
    assert model.auto_update.to == "+15551231234"
    assert model.auto_update.add.first_word == "JOIN"
    assert model.auto_update.remove.first_word == "LEAVE"


def test_group_response_expects_datetime_parsing():
    """Test that ISO 8601 timestamp strings are parsed to datetime objects."""
    model = GroupResponse(
        created_at="2024-06-06T09:22:14.304Z",
        modified_at="2024-06-06T09:22:48.054Z",
    )

    assert model.created_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert model.modified_at == datetime(2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc)


def test_group_response_expects_auto_update_without_keywords():
    """Test that auto_update parses correctly when add and remove are omitted."""
    model = GroupResponse(
        auto_update={"to": "+15551231234"},
    )

    assert model.auto_update.to == "+15551231234"
    assert model.auto_update.add is None
    assert model.auto_update.remove is None


def test_group_response_expects_strict_str_rejects_int():
    """Test that StrictStr fields reject integer values."""
    with pytest.raises(ValidationError):
        GroupResponse(id=123)

    with pytest.raises(ValidationError):
        GroupResponse(name=456)


def test_group_response_expects_strict_int_rejects_str():
    """Test that StrictInt fields reject string values."""
    with pytest.raises(ValidationError):
        GroupResponse(size="two")
