import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.response.dry_run_response import (
    DryRunResponse,
)
from sinch.domains.sms.models.v1.shared import DryRunPerRecipientDetails


@pytest.fixture
def dry_run_response_data():
    """Sample DryRunResponse data with per_recipient details."""
    return {
        "number_of_recipients": 2,
        "number_of_messages": 1,
        "per_recipient": [
            {
                "recipient": "+46701234567",
                "body": "Your order #12345 has been shipped",
                "number_of_parts": 1,
                "encoding": "text",
            },
            {
                "recipient": "+46709876543",
                "body": "Reminder: Your appointment is tomorrow at 2 PM",
                "number_of_parts": 1,
                "encoding": "text",
            },
        ],
    }


@pytest.fixture
def dry_run_response_data_without_per_recipient():
    return {
        "number_of_recipients": 5,
        "number_of_messages": 3,
    }


def test_dry_run_response_expects_valid_input_with_per_recipient(
    dry_run_response_data,
):
    """Test that DryRunResponse correctly parses data with per_recipient details."""
    response = DryRunResponse(**dry_run_response_data)

    assert response.number_of_recipients == 2
    assert response.number_of_messages == 1
    assert response.per_recipient is not None
    assert len(response.per_recipient) == 2

    first_recipient = response.per_recipient[0]
    assert isinstance(first_recipient, DryRunPerRecipientDetails)
    assert first_recipient.recipient == "+46701234567"
    assert first_recipient.body == "Your order #12345 has been shipped"
    assert first_recipient.number_of_parts == 1
    assert first_recipient.encoding == "text"

    second_recipient = response.per_recipient[1]
    assert second_recipient.recipient == "+46709876543"
    assert (
        second_recipient.body
        == "Reminder: Your appointment is tomorrow at 2 PM"
    )
    assert second_recipient.number_of_parts == 1
    assert second_recipient.encoding == "text"


def test_dry_run_response_expects_valid_input_without_per_recipient(
    dry_run_response_data_without_per_recipient,
):
    """Test that DryRunResponse correctly parses data without per_recipient details."""
    response = DryRunResponse(**dry_run_response_data_without_per_recipient)

    assert response.number_of_recipients == 5
    assert response.number_of_messages == 3
    assert response.per_recipient is None
