from datetime import datetime, timezone

from sinch.domains.voice.models.v2.calls.internal.list_calls_response import (
    ListCallsResponse,
)
from sinch.domains.voice.models.v2.shared.call import Call


def test_list_calls_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListCallsResponse(
        calls=[
            {
                "call_id": "01ARZ3NDEKTSV4RRFFQ69G5FAA",
                "project_id": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
                "service_id": "6e124178-c29d-46a5-943c-5c2ae544aade",
                "session_id": "01BX5ZZKBKACTAV9WEVGEMMVRB",
                "start_time": "2025-02-10T09:00:00Z",
                "call_type": "PHONE",
                "direction": "OUTBOUND",
                "call_result": "COMPLETED",
                "origination_type": "SERVER",
                "call_rate": {"currency_code": "USD", "amount": "0.0123"},
                "call_resource_url": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
            }
        ],
        links={
            "first": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=1",
            "last": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=5&pageSize=1",
            "self": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=1",
        },
        meta={"total_count": 1, "page_count": 1},
    )

    assert len(model.calls) == 1
    call = model.calls[0]
    assert isinstance(call, Call)
    assert call.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert call.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert call.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert call.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert call.start_time == datetime(
        2025, 2, 10, 9, 0, 0, tzinfo=timezone.utc
    )
    assert call.call_type == "PHONE"
    assert call.direction == "OUTBOUND"
    assert call.call_result == "COMPLETED"
    assert call.origination_type == "SERVER"
    assert call.call_rate.currency_code == "USD"
    assert call.call_rate.amount == "0.0123"
    assert call.call_resource_url == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA"
    )

    assert model.links.first == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=1"
    )
    assert model.links.last == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=5&pageSize=1"
    )
    assert model.links.self_ == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=1"
    )
    assert model.links.next is None
    assert model.links.prev is None

    assert model.meta.total_count == 1
    assert model.meta.page_count == 1
    assert model.content == model.calls

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert len(alias_dump["calls"]) == 1
    call_dump = alias_dump["calls"][0]
    assert call_dump["callId"] == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert call_dump["projectId"] == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert call_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert call_dump["sessionId"] == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert call_dump["startTime"] == "2025-02-10T09:00:00Z"
    assert call_dump["callType"] == "PHONE"
    assert call_dump["direction"] == "OUTBOUND"
    assert call_dump["callResult"] == "COMPLETED"
    assert call_dump["originationType"] == "SERVER"
    assert call_dump["callRate"] == {
        "currencyCode": "USD",
        "amount": "0.0123",
    }
    assert call_dump["callResourceUrl"] == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA"
    )
    assert alias_dump["links"] == {
        "first": (
            "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=1"
        ),
        "last": (
            "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=5&pageSize=1"
        ),
        "self": (
            "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=1"
        ),
    }
    assert alias_dump["meta"] == {"totalCount": 1, "pageCount": 1}
