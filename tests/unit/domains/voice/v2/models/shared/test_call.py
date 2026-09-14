from datetime import datetime, timezone

from sinch.domains.voice.models.v2.shared.call import Call
from sinch.domains.voice.models.v2.shared.money import Money
from sinch.domains.voice.models.v2.shared.phone import Phone


def test_call_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = Call(
        call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        call_name="origin",
        bridge_name="my-bridge",
        batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC",
        **{"from": {"type": "PHONE", "phone": {"number": "+15551234567"}}},
        to={"type": "PHONE", "phone": {"number": "+15559876543"}},
        start_time="2025-02-10T09:00:00Z",
        update_time="2025-02-10T09:00:10Z",
        call_type="PHONE",
        direction="OUTBOUND",
        answer_time="2025-02-10T09:00:05Z",
        end_time="2025-02-10T09:00:47Z",
        call_duration_seconds=42,
        call_result="COMPLETED",
        call_reason="CALLEE_HANGUP",
        origination_type="SERVER",
        call_rate={"currency_code": "USD", "amount": "0.0123"},
        call_resource_url="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
    )

    assert model.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert model.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert model.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert model.call_name == "origin"
    assert model.bridge_name == "my-bridge"
    assert model.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    assert isinstance(model.from_, Phone)
    assert model.from_.phone.number == "+15551234567"
    assert isinstance(model.to, Phone)
    assert model.to.phone.number == "+15559876543"
    assert model.start_time == datetime(2025, 2, 10, 9, 0, 0, tzinfo=timezone.utc)
    assert model.update_time == datetime(2025, 2, 10, 9, 0, 10, tzinfo=timezone.utc)
    assert model.call_type == "PHONE"
    assert model.direction == "OUTBOUND"
    assert model.answer_time == datetime(2025, 2, 10, 9, 0, 5, tzinfo=timezone.utc)
    assert model.end_time == datetime(2025, 2, 10, 9, 0, 47, tzinfo=timezone.utc)
    assert model.call_duration_seconds == 42
    assert model.call_result == "COMPLETED"
    assert model.call_reason == "CALLEE_HANGUP"
    assert model.origination_type == "SERVER"
    assert isinstance(model.call_rate, Money)
    assert model.call_rate.amount == "0.0123"
    assert model.call_resource_url == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA"
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["callId"] == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert alias_dump["projectId"] == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert alias_dump["sessionId"] == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert alias_dump["callName"] == "origin"
    assert alias_dump["bridgeName"] == "my-bridge"
    assert alias_dump["batchId"] == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    assert alias_dump["startTime"] == "2025-02-10T09:00:00Z"
    assert alias_dump["updateTime"] == "2025-02-10T09:00:10Z"
    assert alias_dump["callType"] == "PHONE"
    assert alias_dump["direction"] == "OUTBOUND"
    assert alias_dump["answerTime"] == "2025-02-10T09:00:05Z"
    assert alias_dump["endTime"] == "2025-02-10T09:00:47Z"
    assert alias_dump["callDurationSeconds"] == 42
    assert alias_dump["callResult"] == "COMPLETED"
    assert alias_dump["callReason"] == "CALLEE_HANGUP"
    assert alias_dump["originationType"] == "SERVER"
    assert alias_dump["callRate"]["amount"] == "0.0123"
    assert alias_dump["callResourceUrl"] == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA"
    )


def test_call_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = Call(
        call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        start_time="2025-02-10T09:00:00Z",
        call_type="PHONE",
        direction="OUTBOUND",
        call_result="COMPLETED",
        origination_type="SERVER",
        call_rate={"currency_code": "USD", "amount": "0.0123"},
        call_resource_url="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
    )

    assert model.call_name is None
    assert model.bridge_name is None
    assert model.batch_id is None
    assert model.from_ is None
    assert model.to is None
    assert model.update_time is None
    assert model.answer_time is None
    assert model.end_time is None
    assert model.call_duration_seconds is None
    assert model.call_reason is None
