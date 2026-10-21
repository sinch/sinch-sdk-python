from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)


def test_conversation_sinch_event_base_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ConversationSinchEventBase(
        app_id="01EB37HMH1M6SV18BSNS3G135H",
        project_id="c36f3d3d-1513-2edd-ae42-11995557ff61",
        accepted_time="2020-11-17T15:09:11Z",
        event_time="2020-11-17T15:09:13Z",
        message_metadata="metadata",
        correlation_id="correlation-1",
    )

    assert model.app_id == "01EB37HMH1M6SV18BSNS3G135H"
    assert model.project_id == "c36f3d3d-1513-2edd-ae42-11995557ff61"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert model.event_time == datetime(
        2020, 11, 17, 15, 9, 13, tzinfo=timezone.utc
    )
    assert model.message_metadata == "metadata"
    assert model.correlation_id == "correlation-1"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "01EB37HMH1M6SV18BSNS3G135H"
    assert alias_dump["project_id"] == "c36f3d3d-1513-2edd-ae42-11995557ff61"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["event_time"] == "2020-11-17T15:09:13Z"
    assert alias_dump["message_metadata"] == "metadata"
    assert alias_dump["correlation_id"] == "correlation-1"


def test_conversation_sinch_event_base_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ConversationSinchEventBase(app_id="app-1", project_id="project-1")

    assert model.accepted_time is None
    assert model.event_time is None
    assert model.message_metadata is None
    assert model.correlation_id is None


def test_conversation_sinch_event_base_expects_validation_error_for_missing_required():
    """Test that app_id and project_id are required."""
    with pytest.raises(ValidationError):
        ConversationSinchEventBase()

