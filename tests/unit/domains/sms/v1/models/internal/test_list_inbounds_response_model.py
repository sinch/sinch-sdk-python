from datetime import datetime, timezone
from sinch.domains.sms.models.v1.internal.list_inbounds_response import ListInboundsResponse
from sinch.domains.sms.models.v1.shared import MOTextMessage


def test_list_inbounds_response_empty_content_expects_empty_list():
    """Test that empty inbounds list returns empty content."""
    model = ListInboundsResponse(count=0, page=0, page_size=30, inbounds=None)

    assert model.count == 0
    assert model.page == 0
    assert model.page_size == 30
    assert model.content == []


def test_list_inbounds_response_expects_correct_mapping():
    """Test that response is handled and mapped to the appropriate fields correctly."""
    data = {
        "count": 2,
        "page": 0,
        "page_size": 2,
        "inbounds": [
            {
                "id": "01FC66621XXXXX119Z8PMV1QPQ",
                "from": "+46701234567",
                "to": "+46709876543",
                "body": "Hello from test",
                "type": "mo_text",
                "received_at": "2024-06-06T09:22:14.304Z",
                "client_reference": "ref-001",
            },
            {
                "id": "01FC66621XXXXX119Z8PMV1QPR",
                "from": "+46701234568",
                "to": "+46709876543",
                "body": "Second message",
                "type": "mo_text",
                "received_at": "2024-06-06T09:25:00.000Z",
            },
        ],
    }
    response = ListInboundsResponse(**data)

    assert response.count == 2
    assert response.page == 0
    assert response.page_size == 2

    content = response.content
    assert isinstance(content, list)
    assert len(content) == 2

    first = content[0]
    assert isinstance(first, MOTextMessage)
    assert first.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert first.from_ == "+46701234567"
    assert first.body == "Hello from test"
    assert first.received_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert first.client_reference == "ref-001"

    second = content[1]
    assert isinstance(second, MOTextMessage)
    assert second.id == "01FC66621XXXXX119Z8PMV1QPR"
    assert second.body == "Second message"
    assert second.client_reference is None
