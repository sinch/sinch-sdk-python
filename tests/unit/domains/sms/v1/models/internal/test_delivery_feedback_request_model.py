import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.internal import DeliveryFeedbackRequest


@pytest.fixture
def sample_delivery_feedback_request_data():
    return {
        "batch_id": "01W4FFL35P4NC4K35SMSBATCH3",
        "recipients": ["+46876543210", "+46987654321"],
    }


def test_delivery_feedback_request_expects_valid_inputs(
    sample_delivery_feedback_request_data,
):
    """Test DeliveryFeedbackRequest with valid inputs."""
    request = DeliveryFeedbackRequest(**sample_delivery_feedback_request_data)
    assert (
        request.batch_id == sample_delivery_feedback_request_data["batch_id"]
    )
    assert (
        request.recipients
        == sample_delivery_feedback_request_data["recipients"]
    )


def test_delivery_feedback_request_expects_single_recipient():
    """Test DeliveryFeedbackRequest with a single recipient."""
    request = DeliveryFeedbackRequest(
        batch_id="01W4FFL35P4NC4K35SMSBATCH3",
        recipients=["+46876543210"],
    )
    assert request.batch_id == "01W4FFL35P4NC4K35SMSBATCH3"
    assert len(request.recipients) == 1
    assert request.recipients[0] == "+46876543210"


def test_delivery_feedback_request_expects_empty_recipients_list():
    """Test DeliveryFeedbackRequest with empty recipients list."""
    request = DeliveryFeedbackRequest(
        batch_id="01W4FFL35P4NC4K35SMSBATCH3",
        recipients=[],
    )
    assert request.batch_id == "01W4FFL35P4NC4K35SMSBATCH3"
    assert request.recipients == []


@pytest.mark.parametrize(
    "missing_field",
    ["batch_id", "recipients"],
)
def test_delivery_feedback_request_expects_required_fields(
    sample_delivery_feedback_request_data, missing_field
):
    """Test that DeliveryFeedbackRequest requires batch_id and recipients fields."""
    data = sample_delivery_feedback_request_data.copy()
    data.pop(missing_field)
    with pytest.raises(ValidationError) as exc_info:
        DeliveryFeedbackRequest(**data)
    assert missing_field in str(exc_info.value)


@pytest.mark.parametrize(
    "invalid_batch_id",
    [12345, None],
)
def test_delivery_feedback_request_expects_batch_id_must_be_string(
    invalid_batch_id,
):
    """Test that batch_id must be a string."""
    with pytest.raises(ValidationError):
        DeliveryFeedbackRequest(
            batch_id=invalid_batch_id,
            recipients=["+46876543210"],
        )


@pytest.mark.parametrize(
    "invalid_recipients",
    ["+46876543210", [123, 456], ["+46876543210", None]],
)
def test_delivery_feedback_request_expects_recipients_must_be_list_of_strings(
    invalid_recipients,
):
    """Test that recipients must be a list of strings."""
    with pytest.raises(ValidationError):
        DeliveryFeedbackRequest(
            batch_id="01W4FFL35P4NC4K35SMSBATCH3",
            recipients=invalid_recipients,
        )
