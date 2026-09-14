from datetime import datetime, timezone

from sinch.domains.voice.models.v2.batches.response.batch_summary_response import (
    BatchSummaryResponse,
)


def test_batch_summary_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = BatchSummaryResponse(
        batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC",
        session_count=3,
        end_time="2025-02-10T09:00:47Z",
        queued=1,
        in_progress=1,
        completed=1,
        expired=0,
        ttl_seconds=3600,
        requested_cps=10,
    )

    assert model.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    assert model.session_count == 3
    assert model.end_time == datetime(2025, 2, 10, 9, 0, 47, tzinfo=timezone.utc)
    assert model.queued == 1
    assert model.in_progress == 1
    assert model.completed == 1
    assert model.expired == 0
    assert model.ttl_seconds == 3600
    assert model.requested_cps == 10

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["batchId"] == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    assert alias_dump["sessionCount"] == 3
    assert alias_dump["endTime"] == "2025-02-10T09:00:47Z"
    assert alias_dump["queued"] == 1
    assert alias_dump["inProgress"] == 1
    assert alias_dump["completed"] == 1
    assert alias_dump["expired"] == 0
    assert alias_dump["ttlSeconds"] == 3600
    assert alias_dump["requestedCps"] == 10


def test_batch_summary_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = BatchSummaryResponse(
        batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC",
        session_count=3,
        queued=1,
        in_progress=1,
        completed=1,
        expired=0,
        requested_cps=10,
    )

    assert model.end_time is None
    assert model.ttl_seconds is None
