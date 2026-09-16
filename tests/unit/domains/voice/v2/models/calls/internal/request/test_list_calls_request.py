from datetime import datetime

from sinch.domains.voice.models.v2.calls.internal.request.list_calls_request import (
    ListCallsRequest,
)


def test_list_calls_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListCallsRequest(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        from_="+15551234567",
        to="+15551234568",
        call_type="PHONE",
        start_time=datetime(2025, 2, 1, 14, 0, 0),
        end_time=datetime(2025, 3, 1, 14, 0, 0),
        call_result="COMPLETED",
        call_reason="CALLEE_HANGUP",
        page_size=20,
        page=2,
    )

    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert model.from_ == "+15551234567"
    assert model.to == "+15551234568"
    assert model.call_type == "PHONE"
    assert model.start_time == datetime(2025, 2, 1, 14, 0, 0)
    assert model.end_time == datetime(2025, 3, 1, 14, 0, 0)
    assert model.call_result == "COMPLETED"
    assert model.call_reason == "CALLEE_HANGUP"
    assert model.page_size == 20
    assert model.page == 2

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert alias_dump["from"] == "+15551234567"
    assert alias_dump["callType"] == "PHONE"
    assert alias_dump["startTime"] == "2025-02-01T14:00:00"
    assert alias_dump["endTime"] == "2025-03-01T14:00:00"
    assert alias_dump["callResult"] == "COMPLETED"
    assert alias_dump["callReason"] == "CALLEE_HANGUP"
    assert alias_dump["pageSize"] == 20
    assert alias_dump["to"] == "+15551234568"
    assert alias_dump["page"] == 2


def test_list_calls_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListCallsRequest()

    assert model.service_id is None
    assert model.from_ is None
    assert model.to is None
    assert model.call_type is None
    assert model.start_time is None
    assert model.end_time is None
    assert model.call_result is None
    assert model.call_reason is None
    assert model.page_size is None
    assert model.page is None
