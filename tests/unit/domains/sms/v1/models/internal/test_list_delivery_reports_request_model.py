from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.internal import ListDeliveryReportsRequest


def test_list_delivery_reports_request_expects_defaults():
    """Test that the model correctly sets default values."""
    model = ListDeliveryReportsRequest()
    assert model.page is None
    assert model.page_size is None
    assert model.start_date is None
    assert model.end_date is None
    assert model.status is None
    assert model.code is None
    assert model.client_reference is None


def test_list_delivery_reports_request_expects_parsed_input():
    """Test that the model correctly parses input with all parameters."""
    start = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2025, 1, 8, 12, 0, 0, tzinfo=timezone.utc)

    model = ListDeliveryReportsRequest(
        page=1,
        page_size=50,
        start_date=start,
        end_date=end,
        status=["DELIVERED", "FAILED"],
        code=[401, 402],
        client_reference="my-client-ref",
    )

    assert model.page == 1
    assert model.page_size == 50
    assert model.start_date == start
    assert model.end_date == end
    assert model.status == ["DELIVERED", "FAILED"]
    assert model.code == [401, 402]
    assert model.client_reference == "my-client-ref"
