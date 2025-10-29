from datetime import datetime, timedelta, timezone
import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.internal import ListDeliveryReportsRequest


def test_list_delivery_reports_request_expects_defaults():
    """Test that the model correctly sets default values."""
    model = ListDeliveryReportsRequest()
    assert model.page == 0
    assert model.page_size == 30
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


@pytest.mark.parametrize(
    "page, expected_error",
    [
        (-1, ValidationError),
        (-10, ValidationError),
    ],
)
def test_list_delivery_reports_request_expects_validation_error_for_invalid_page(
    page, expected_error
):
    """Test that invalid page values raise ValidationError."""
    with pytest.raises(expected_error):
        ListDeliveryReportsRequest(page=page)


@pytest.mark.parametrize(
    "page_size, expected_error",
    [
        (0, ValidationError),
        (101, ValidationError),
        (-1, ValidationError),
    ],
)
def test_list_delivery_reports_request_expects_validation_error_for_invalid_page_size(
    page_size, expected_error
):
    """Test that invalid page_size values raise ValidationError."""
    with pytest.raises(expected_error):
        ListDeliveryReportsRequest(page_size=page_size)
