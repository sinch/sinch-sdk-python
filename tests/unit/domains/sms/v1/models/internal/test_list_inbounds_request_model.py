from datetime import datetime, timezone
from sinch.domains.sms.models.v1.internal.list_inbounds_request import ListInboundsRequest


def test_list_inbounds_request_expects_defaults():
    """Test that the model correctly sets default values."""
    model = ListInboundsRequest()

    assert model.page is None
    assert model.page_size is None
    assert model.to is None
    assert model.start_date is None
    assert model.end_date is None
    assert model.client_reference is None


def test_list_inbounds_request_expects_parsed_input():
    """Test that the model correctly parses input with all parameters."""
    start = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2025, 1, 8, 12, 0, 0, tzinfo=timezone.utc)

    model = ListInboundsRequest(
        page=1,
        page_size=50,
        to=["+46701234567", "+46709876543"],
        start_date=start,
        end_date=end,
        client_reference="my-client-ref",
    )

    assert model.page == 1
    assert model.page_size == 50
    assert model.to == ["+46701234567", "+46709876543"]
    assert model.start_date == start
    assert model.end_date == end
    assert model.client_reference == "my-client-ref"
