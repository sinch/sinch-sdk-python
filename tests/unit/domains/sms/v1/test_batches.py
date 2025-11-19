from datetime import datetime, timezone
from unittest.mock import MagicMock
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.pagination import SMSPaginator
from sinch.domains.sms.api.v1.batches_apis import Batches
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.api.v1.internal import (
    CancelBatchMessageEndpoint,
    DryRunEndpoint,
    GetBatchMessageEndpoint,
    ListBatchesEndpoint,
    ReplaceBatchEndpoint,
    SendSMSEndpoint,
    DeliveryFeedbackEndpoint,
    UpdateBatchMessageEndpoint,
)
from sinch.domains.sms.models.v1.internal.dry_run_request import (
    DryRunTextRequest,
    DryRunBinaryRequest,
    DryRunMediaRequest,
)
from sinch.domains.sms.models.v1.internal.replace_batch_request import (
    ReplaceTextRequest,
    ReplaceBinaryRequest,
    ReplaceMediaRequest,
)
from sinch.domains.sms.models.v1.internal.update_batch_message_request import (
    UpdateTextRequestWithBatchId,
    UpdateBinaryRequestWithBatchId,
    UpdateMediaRequestWithBatchId,
)
from sinch.domains.sms.models.v1.response.dry_run_response import (
    DryRunResponse,
)
from sinch.domains.sms.models.v1.response.list_batches_response import (
    ListBatchesResponse,
)
from sinch.domains.sms.models.v1.shared import (
    MediaBody,
    DryRunPerRecipientDetails,
    TextRequest,
    BinaryRequest,
    MediaRequest,
)
from sinch.domains.sms.models.v1.shared.text_response import TextResponse
from sinch.domains.sms.models.v1.shared.binary_response import BinaryResponse
from sinch.domains.sms.models.v1.shared.media_response import MediaResponse


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


@pytest.fixture
def mock_batch_response():
    """Sample BatchResponse (TextResponse) for testing."""
    return TextResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        canceled=False,
        body="Test message",
        type="mt_text",
        created_at=datetime(
            2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
        ),
        modified_at=datetime(
            2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
        ),
    )


def test_batches_cancel_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that cancel sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_batch_response
    )

    spy_endpoint = mocker.spy(CancelBatchMessageEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.cancel(batch_id="01FC66621XXXXX119Z8PMV1QPQ")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].batch_id == "01FC66621XXXXX119Z8PMV1QPQ"

    assert isinstance(response, TextResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_get_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that get sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_batch_response
    )

    spy_endpoint = mocker.spy(GetBatchMessageEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.get(batch_id="01FC66621XXXXX119Z8PMV1QPQ")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].batch_id == "01FC66621XXXXX119Z8PMV1QPQ"

    assert isinstance(response, TextResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_list_expects_correct_request(
    mock_sinch_client_sms, mocker
):
    """Test that list sends the correct request and returns a paginator."""
    mock_list_batches_response = ListBatchesResponse(
        count=2,
        page=0,
        page_size=10,
        batches=[],
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_list_batches_response
    )

    spy_endpoint = mocker.spy(ListBatchesEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    paginator = batches.list(
        page=0,
        page_size=10,
        start_date=datetime(2024, 6, 1, tzinfo=timezone.utc),
        end_date=datetime(2024, 6, 30, tzinfo=timezone.utc),
        from_=["+46701111111"],
        client_reference="test-ref",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].page == 0
    assert kwargs["request_data"].page_size == 10
    assert kwargs["request_data"].from_ == ["+46701111111"]
    assert kwargs["request_data"].client_reference == "test-ref"

    assert isinstance(paginator, SMSPaginator)
    assert paginator.result == mock_list_batches_response


def test_batches_send_sms_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that send_sms sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_batch_response
    )

    spy_endpoint = mocker.spy(SendSMSEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.send_sms(
        to=["+46701234567", "+46709876543"],
        from_="+46701111111",
        body="Test message",
        delivery_report="full",
        send_at=datetime(2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc),
        expire_at=datetime(2024, 6, 10, 9, 25, 0, tzinfo=timezone.utc),
        callback_url="https://example.com/callback",
        client_reference="test-ref",
        feedback_enabled=True,
        flash_message=False,
        max_number_of_message_parts=3,
        truncate_concat=True,
        from_ton=1,
        from_npi=1,
        parameters={"name": {"+46701234567": "John"}},
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], TextRequest)
    assert kwargs["request_data"].to == ["+46701234567", "+46709876543"]
    assert kwargs["request_data"].from_ == "+46701111111"
    assert kwargs["request_data"].body == "Test message"
    assert kwargs["request_data"].delivery_report == "full"
    assert kwargs["request_data"].feedback_enabled is True
    assert kwargs["request_data"].flash_message is False
    assert kwargs["request_data"].max_number_of_message_parts == 3
    assert kwargs["request_data"].truncate_concat is True
    assert kwargs["request_data"].from_ton == 1
    assert kwargs["request_data"].from_npi == 1
    assert kwargs["request_data"].parameters == {"name": {"+46701234567": "John"}}

    assert isinstance(response, TextResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_send_binary_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that send_binary sends the correct request and handles the response properly."""
    mock_binary_response = BinaryResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        canceled=False,
        body="SGVsbG8gV29ybGQh",
        udh="06050423F423F4",
        type="mt_binary",
        created_at=datetime(
            2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
        ),
        modified_at=datetime(
            2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
        ),
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_binary_response
    )

    spy_endpoint = mocker.spy(SendSMSEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.send_binary(
        to=["+46701234567"],
        from_="+46701111111",
        body="SGVsbG8gV29ybGQh",
        udh="06050423F423F4",
        delivery_report="summary",
        send_at=datetime(2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc),
        expire_at=datetime(2024, 6, 10, 9, 25, 0, tzinfo=timezone.utc),
        callback_url="https://example.com/callback",
        client_reference="test-ref",
        feedback_enabled=True,
        from_ton=1,
        from_npi=1,
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], BinaryRequest)
    assert kwargs["request_data"].to == ["+46701234567"]
    assert kwargs["request_data"].from_ == "+46701111111"
    assert kwargs["request_data"].body == "SGVsbG8gV29ybGQh"
    assert kwargs["request_data"].udh == "06050423F423F4"
    assert kwargs["request_data"].delivery_report == "summary"
    assert kwargs["request_data"].feedback_enabled is True
    assert kwargs["request_data"].from_ton == 1
    assert kwargs["request_data"].from_npi == 1

    assert isinstance(response, BinaryResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_send_mms_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that send_mms sends the correct request and handles the response properly."""
    mock_media_response = MediaResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        canceled=False,
        body=MediaBody(
            url="https://capybara.com/image.jpg",
            message="Check out this image!",
            subject="Image",
        ),
        type="mt_media",
        created_at=datetime(
            2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
        ),
        modified_at=datetime(
            2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
        ),
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_media_response
    )

    spy_endpoint = mocker.spy(SendSMSEndpoint, "__init__")

    media_body = MediaBody(
        url="https://capybara.com/video.mp4",
        message="Check out this video!",
        subject="Video",
    )

    batches = Batches(mock_sinch_client_sms)
    response = batches.send_mms(
        to=["+46701234567"],
        from_="+46701111111",
        body=media_body,
        delivery_report="full",
        send_at=datetime(2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc),
        expire_at=datetime(2024, 6, 10, 9, 25, 0, tzinfo=timezone.utc),
        callback_url="https://example.com/callback",
        client_reference="test-ref",
        feedback_enabled=True,
        strict_validation=True,
        parameters={"name": {"+46701234567": "John"}},
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], MediaRequest)
    assert kwargs["request_data"].to == ["+46701234567"]
    assert kwargs["request_data"].from_ == "+46701111111"
    assert isinstance(kwargs["request_data"].body, MediaBody)
    assert kwargs["request_data"].body.url == "https://capybara.com/video.mp4"
    assert kwargs["request_data"].body.message == "Check out this video!"
    assert kwargs["request_data"].body.subject == "Video"
    assert kwargs["request_data"].delivery_report == "full"
    assert kwargs["request_data"].feedback_enabled is True
    assert kwargs["request_data"].strict_validation is True
    assert kwargs["request_data"].parameters == {"name": {"+46701234567": "John"}}

    assert isinstance(response, MediaResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_dry_run_sms_expects_correct_request(
    mock_sinch_client_sms, mock_dry_run_response, mocker
):
    """Test that dry_run_sms sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_dry_run_response
    )

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


def test_batches_dry_run_with_request_object_expects_correct_request(
    mock_sinch_client_sms, mock_dry_run_response, mocker
):
    """Test that dry_run with DryRunRequest object sends the correct request."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_dry_run_response
    )

    spy_endpoint = mocker.spy(DryRunEndpoint, "__init__")

    request = DryRunTextRequest(
        to=["+46701234567"],
        from_="+46701111111",
        body="Hello World!",
        per_recipient=True,
        number_of_recipients=100,
    )

    batches = Batches(mock_sinch_client_sms)
    response = batches.dry_run(request=request)

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


def test_batches_replace_sms_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that replace_sms sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_batch_response
    )

    spy_endpoint = mocker.spy(ReplaceBatchEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.replace_sms(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        body="Updated message",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ReplaceTextRequest)
    assert kwargs["request_data"].batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert kwargs["request_data"].to == ["+46701234567"]
    assert kwargs["request_data"].from_ == "+46701111111"
    assert kwargs["request_data"].body == "Updated message"

    assert isinstance(response, TextResponse)
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_replace_binary_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that replace_binary sends the correct request and handles the response properly."""
    mock_binary_response = BinaryResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        canceled=False,
        body="SGVsbG8gV29ybGQh",
        udh="06050423F423F4",
        type="mt_binary",
        created_at=datetime(
            2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
        ),
        modified_at=datetime(
            2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
        ),
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_binary_response
    )

    spy_endpoint = mocker.spy(ReplaceBatchEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.replace_binary(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        body="SGVsbG8gV29ybGQh",
        udh="06050423F423F4",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ReplaceBinaryRequest)
    assert kwargs["request_data"].batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert kwargs["request_data"].udh == "06050423F423F4"

    assert isinstance(response, BinaryResponse)
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_replace_mms_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that replace_mms sends the correct request and handles the response properly."""
    mock_media_response = MediaResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        canceled=False,
        body=MediaBody(
            url="https://capybara.com/image.jpg",
            message="Check out this image!",
            subject="Image",
        ),
        type="mt_media",
        created_at=datetime(
            2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
        ),
        modified_at=datetime(
            2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
        ),
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_media_response
    )

    spy_endpoint = mocker.spy(ReplaceBatchEndpoint, "__init__")

    media_body = MediaBody(
        url="https://capybara.com/video.mp4",
        message="Updated video message",
        subject="Video Update",
    )

    batches = Batches(mock_sinch_client_sms)
    response = batches.replace_mms(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        body=media_body,
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ReplaceMediaRequest)
    assert kwargs["request_data"].batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert isinstance(kwargs["request_data"].body, MediaBody)
    assert kwargs["request_data"].body.url == "https://capybara.com/video.mp4"

    assert isinstance(response, MediaResponse)
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_send_delivery_feedback_expects_correct_request(
    mock_sinch_client_sms, mocker
):
    """Test that send_delivery_feedback sends the correct request."""
    mock_sinch_client_sms.configuration.transport.request.return_value = None

    spy_endpoint = mocker.spy(DeliveryFeedbackEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    batches.send_delivery_feedback(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        recipients=["+46701234567", "+46709876543"],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert kwargs["request_data"].recipients == [
        "+46701234567",
        "+46709876543",
    ]

    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_update_sms_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that update_sms sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_batch_response
    )

    spy_endpoint = mocker.spy(UpdateBatchMessageEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.update_sms(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        body="Updated body",
        to_add=["+46709999999"],
        to_remove=["+46708888888"],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], UpdateTextRequestWithBatchId)
    assert kwargs["request_data"].batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert kwargs["request_data"].body == "Updated body"
    assert kwargs["request_data"].to_add == ["+46709999999"]
    assert kwargs["request_data"].to_remove == ["+46708888888"]

    assert isinstance(response, TextResponse)
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_update_binary_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that update_binary sends the correct request and handles the response properly."""
    mock_binary_response = BinaryResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        canceled=False,
        body="VXBkYXRlZA==",
        udh="06050423F423F5",
        type="mt_binary",
        created_at=datetime(
            2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
        ),
        modified_at=datetime(
            2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
        ),
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_binary_response
    )

    spy_endpoint = mocker.spy(UpdateBatchMessageEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.update_binary(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        udh="06050423F423F5",
        body="VXBkYXRlZA==",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], UpdateBinaryRequestWithBatchId)
    assert kwargs["request_data"].batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert kwargs["request_data"].udh == "06050423F423F5"
    assert kwargs["request_data"].body == "VXBkYXRlZA=="

    assert isinstance(response, BinaryResponse)
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_update_mms_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that update_mms sends the correct request and handles the response properly."""
    mock_media_response = MediaResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        canceled=False,
        body=MediaBody(
            url="https://capybara.com/updated.jpg",
            message="Updated message",
            subject="Updated",
        ),
        type="mt_media",
        created_at=datetime(
            2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
        ),
        modified_at=datetime(
            2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
        ),
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_media_response
    )

    spy_endpoint = mocker.spy(UpdateBatchMessageEndpoint, "__init__")

    media_body = MediaBody(
        url="https://capybara.com/new-image.jpg",
        message="New image message",
        subject="New Image",
    )

    batches = Batches(mock_sinch_client_sms)
    response = batches.update_mms(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        body=media_body,
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], UpdateMediaRequestWithBatchId)
    assert kwargs["request_data"].batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert isinstance(kwargs["request_data"].body, MediaBody)
    assert (
        kwargs["request_data"].body.url == "https://capybara.com/new-image.jpg"
    )

    assert isinstance(response, MediaResponse)
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_send_expects_correct_request(
    mock_sinch_client_sms, mock_batch_response, mocker
):
    """Test that send with TextRequest sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_batch_response
    )

    spy_endpoint = mocker.spy(SendSMSEndpoint, "__init__")

    batches = Batches(mock_sinch_client_sms)
    response = batches.send(
        request={
            "to": ["+46701234567"],
            "from_": "+46701111111",
            "body": "Test message",
            "type": "mt_text",
        }
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].to == ["+46701234567"]
    assert kwargs["request_data"].from_ == "+46701111111"
    assert kwargs["request_data"].body == "Test message"

    assert isinstance(response, TextResponse)
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_batches_expects_validation_recalculates_auth_method_when_credentials_change(
    mock_sinch_client_sms,
):
    """Test that SMS requests validate authentication and recalculate auth method when credentials change after initialization."""
    config = mock_sinch_client_sms.configuration

    assert config.authentication_method == "project_auth"

    mock_response = TextResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        to=["+46701234567"],
        from_="+46701111111",
        canceled=False,
        body="Test message",
        type="mt_text",
        created_at=datetime(
            2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
        ),
        modified_at=datetime(
            2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
        ),
    )
    config.transport.request.return_value = mock_response

    config.sms_api_token = "test_sms_token"

    assert config.authentication_method == "project_auth"

    # Make an SMS request. This should trigger validation and recalculate auth method
    batches = Batches(mock_sinch_client_sms)
    response = batches.get(batch_id="01FC66621XXXXX119Z8PMV1QPQ")

    assert config.authentication_method == "sms_auth"
    assert isinstance(response, TextResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
