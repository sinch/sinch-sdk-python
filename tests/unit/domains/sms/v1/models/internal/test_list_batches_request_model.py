from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.internal import ListBatchesRequest


def test_list_batches_request_expects_defaults():
    """Test that the model correctly sets default values."""
    model = ListBatchesRequest()
    assert model.page is None
    assert model.page_size is None
    assert model.start_date is None
    assert model.end_date is None
    assert model.from_ is None
    assert model.client_reference is None


def test_list_batches_request_expects_parsed_input():
    """Test that the model correctly parses input with all parameters."""
    start = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2025, 1, 8, 12, 0, 0, tzinfo=timezone.utc)

    model = ListBatchesRequest(
        page=1,
        page_size=50,
        start_date=start,
        end_date=end,
        from_=["+46701234567", "+46709876543"],
        client_reference="my-client-ref",
    )

    assert model.page == 1
    assert model.page_size == 50
    assert model.start_date == start
    assert model.end_date == end
    assert model.from_ == ["+46701234567", "+46709876543"]
    assert model.client_reference == "my-client-ref"


def test_list_batches_request_expects_from_alias():
    """Test that the 'from' alias works correctly."""
    model = ListBatchesRequest(from_=["+46701234567"])

    assert model.from_ == ["+46701234567"]

    # Check that model_dump with by_alias=True uses "from"
    dumped = model.model_dump(exclude_none=True, by_alias=True)
    assert "from" in dumped
    assert dumped["from"] == ["+46701234567"]
    assert "from_" not in dumped

    # Check that model_dump with by_alias=False uses "from_"
    dumped_no_alias = model.model_dump(exclude_none=True, by_alias=False)
    assert "from_" in dumped_no_alias
    assert dumped_no_alias["from_"] == ["+46701234567"]
    assert "from" not in dumped_no_alias


def test_list_batches_request_expects_partial_input():
    """Test that the model works with partial input."""
    model = ListBatchesRequest(page=2, page_size=20)

    assert model.page == 2
    assert model.page_size == 20
    assert model.start_date is None
    assert model.end_date is None
    assert model.from_ is None
    assert model.client_reference is None


def test_list_batches_request_expects_empty_from_list():
    """Test that from_ can be an empty list."""
    model = ListBatchesRequest(from_=[])

    assert model.from_ == []



