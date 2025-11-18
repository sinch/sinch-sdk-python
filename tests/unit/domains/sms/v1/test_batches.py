import pytest
from sinch.domains.sms.api.v1.batches_apis import Batches
from sinch.domains.sms.api.v1.internal import DryRunEndpoint
from sinch.domains.sms.models.v1.internal.dry_run_request import (
    DryRunTextRequest,
    DryRunBinaryRequest,
    DryRunMediaRequest,
)
from sinch.domains.sms.models.v1.response.dry_run_response import (
    DryRunResponse,
)
from sinch.domains.sms.models.v1.shared import (
    MediaBody,
    DryRunPerRecipientDetails,
)


@pytest.fixture
def mock_dry_run_response():
    """Sample DryRunResponse for testing."""
    return DryRunResponse(
        number_of_recipients=2,
        number_of_messages=1,
        per_recipient=[
            DryRunPerRecipientDetails(
                recipient="+46701234567",
                body="Hello World!",
                number_of_parts=1,
                encoding="text",
            ),
            DryRunPerRecipientDetails(
                recipient="+46709876543",
                body="Hello World!",
                number_of_parts=1,
                encoding="text",
            ),
        ],
    )


def test_batches_dry_run_sms_expects_correct_request(
    mock_sinch_client_sms, mock_dry_run_response, mocker
):
    """Test that dry_run_sms sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_dry_run_response
    )

    # Spy on the DryRunEndpoint to capture calls
    spy_endpoint = mocker.spy(DryRunEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.dry_run_sms(
        to=["+46701234567"],
        from_="+46701111111",
        body="Hello World!",
        per_recipient=True,
        number_of_recipients=100,
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], DryRunTextRequest)
    assert kwargs["request_data"].to == ["+46701234567"]
    assert kwargs["request_data"].from_ == "+46701111111"
    assert kwargs["request_data"].body == "Hello World!"
    assert kwargs["request_data"].per_recipient is True
    assert kwargs["request_data"].number_of_recipients == 100

    assert isinstance(response, DryRunResponse)
    assert response.number_of_recipients == 2
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_dry_run_binary_expects_correct_request(
    mock_sinch_client_sms, mock_dry_run_response, mocker
):
    """Test that dry_run_binary sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_dry_run_response
    )

    spy_endpoint = mocker.spy(DryRunEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.dry_run_binary(
        to=["+46701234567"],
        from_="+46701111111",
        body="SGVsbG8gV29ybGQh",
        udh="06050423F423F4",
        per_recipient=False,
        number_of_recipients=50,
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], DryRunBinaryRequest)
    assert kwargs["request_data"].udh == "06050423F423F4"
    assert kwargs["request_data"].per_recipient is False
    assert kwargs["request_data"].number_of_recipients == 50

    assert isinstance(response, DryRunResponse)
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_dry_run_mms_expects_correct_request(
    mock_sinch_client_sms, mock_dry_run_response, mocker
):
    """Test that dry_run_mms sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_dry_run_response
    )

    spy_endpoint = mocker.spy(DryRunEndpoint, "__init__")

    media_body = MediaBody(
        url="https://capybara.com/image.jpg",
        message="Check out this image!",
        subject="Image",
    )

    batches = Batches(mock_sinch_client_sms)
    response = batches.dry_run_mms(
        to=["+46701234567"],
        from_="+46701111111",
        body=media_body,
        per_recipient=True,
        number_of_recipients=75,
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], DryRunMediaRequest)
    assert isinstance(kwargs["request_data"].body, MediaBody)
    assert kwargs["request_data"].body.url == "https://capybara.com/image.jpg"
    assert kwargs["request_data"].per_recipient is True
    assert kwargs["request_data"].number_of_recipients == 75

    assert isinstance(response, DryRunResponse)
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()
