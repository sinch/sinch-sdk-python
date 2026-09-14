from datetime import datetime, timezone

from sinch.domains.voice.models.v2.sessions.response.session_response import (
    SessionResponse,
)
from sinch.domains.voice.models.v2.shared.call import Call


def test_session_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SessionResponse(
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        calls=[Call(
            session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
            project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
            call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA",
            start_time="2025-02-10T09:00:00Z",
            call_type="PHONE",
            direction="OUTBOUND",
            call_result="COMPLETED",
            origination_type="SERVER",
            call_rate={"currency_code": "USD", "amount": "0.0123"},
            call_resource_url="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
        )],
        create_time="2025-02-10T09:00:00Z",
        update_time="2025-02-10T09:00:30Z",
        end_time="2025-02-10T09:00:47Z",
        state="COMPLETED",
    )

    assert model.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert model.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert len(model.calls) == 1
    assert isinstance(model.calls[0], Call)
    call = model.calls[0]
    assert call.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert call.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert call.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert call.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert call.start_time == datetime(2025, 2, 10, 9, 0, 0, tzinfo=timezone.utc)
    assert call.call_type == "PHONE"
    assert call.direction == "OUTBOUND"
    assert call.call_result == "COMPLETED"
    assert call.origination_type == "SERVER"
    assert call.call_rate.currency_code == "USD"
    assert call.call_rate.amount == "0.0123"
    assert call.call_resource_url == (
        "https://voice.api.sinch.com/v2/projects/"
        "5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/"
        "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    )
    assert model.state == "COMPLETED"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["sessionId"] == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert alias_dump["projectId"] == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert len(alias_dump["calls"]) == 1
    assert alias_dump["state"] == "COMPLETED"


def test_session_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = SessionResponse(
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        calls=[],
        create_time="2025-02-10T09:00:00Z",
        state="COMPLETED",
    )

    assert model.update_time is None
    assert model.end_time is None
