import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.pagination import SMSPaginator
from sinch.domains.sms.api.v1 import DeliveryReports
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.api.v1.internal import (
    GetBatchDeliveryReportEndpoint,
    GetRecipientDeliveryReportEndpoint,
    ListDeliveryReportsEndpoint,
)
from sinch.domains.sms.models.v1.internal import (
    GetBatchDeliveryReportRequest,
    GetRecipientDeliveryReportRequest,
    ListDeliveryReportsRequest,
    ListDeliveryReportsResponse,
)
from sinch.domains.sms.models.v1.response import (
    BatchDeliveryReport,
    RecipientDeliveryReport,
)
from sinch.domains.sms.models.v1.shared import MessageDeliveryStatus


def test_get_batch_delivery_report_expects_valid_request(
    mock_sinch_client_sms, mocker
):
    """
    Test that the DeliveryReports.get() method sends the correct request
    and handles the response properly.
    """
    mock_response = BatchDeliveryReport(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        statuses=[
            MessageDeliveryStatus(code=400, count=1, status="DELIVERED")
        ],
        total_message_count=1,
        type="summary",
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_response
    )

    # Spy on the GetBatchDeliveryReportEndpoint to capture calls
    spy_endpoint = mocker.spy(GetBatchDeliveryReportEndpoint, "__init__")

    delivery_reports = DeliveryReports(mock_sinch_client_sms)
    response = delivery_reports.get(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        report_type="summary",
        status=["DELIVERED"],
        code=[400],
        client_reference="test_client_ref",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == GetBatchDeliveryReportRequest(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        type="summary",
        status=["DELIVERED"],
        code=[400],
        client_reference="test_client_ref",
    )

    assert isinstance(response, BatchDeliveryReport)
    assert response.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_get_for_number_expects_correct_request(mock_sinch_client_sms, mocker):
    """
    Test that the DeliveryReports.get_for_number() method sends the correct request
    and handles the response properly.
    """
    from datetime import datetime, timezone

    mock_response = RecipientDeliveryReport(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        recipient="+1234567890",
        code=400,
        status="DELIVERED",
        type="recipient_delivery_report_sms",
        at=datetime(2025, 1, 15, 10, 30, 45, 123000, tzinfo=timezone.utc),
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_response
    )

    spy_endpoint = mocker.spy(GetRecipientDeliveryReportEndpoint, "__init__")

    delivery_reports = DeliveryReports(mock_sinch_client_sms)
    response = delivery_reports.get_for_number(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ", recipient="+1234567890"
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == GetRecipientDeliveryReportRequest(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ", recipient_msisdn="+1234567890"
    )

    assert isinstance(response, RecipientDeliveryReport)
    assert response.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert response.recipient == "+1234567890"


def test_list_delivery_reports_expects_valid_request(
    mock_sinch_client_sms, mocker
):
    """
    Test that the DeliveryReports.list() method sends the correct request
    and handles the response properly.
    """
    from datetime import datetime, timezone

    mock_response = ListDeliveryReportsResponse(
        page=0, page_size=2, count=1, delivery_reports=[]
    )
    mock_sinch_client_sms.configuration.transport.request.return_value = (
        mock_response
    )

    spy_endpoint = mocker.spy(ListDeliveryReportsEndpoint, "__init__")

    delivery_reports = DeliveryReports(mock_sinch_client_sms)
    response = delivery_reports.list(
        page=0,
        page_size=2,
        start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2025, 1, 31, tzinfo=timezone.utc),
        status=["DELIVERED"],
        code=[400],
        client_reference="test_client_ref",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == ListDeliveryReportsRequest(
        page=0,
        page_size=2,
        start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2025, 1, 31, tzinfo=timezone.utc),
        status=["DELIVERED"],
        code=[400],
        client_reference="test_client_ref",
    )

    assert isinstance(response, SMSPaginator)
    assert hasattr(response, "has_next_page")
    assert response.result == mock_response
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_sms_endpoint_handle_response_raises_exception_on_error(mock_sinch_client_sms):
    """
    Test that SmsEndpoint.handle_response raises SmsException when status_code >= 400.
    """
    
    request_data = GetBatchDeliveryReportRequest(
        batch_id="test_batch_id",
        type="summary"
    )
    endpoint = GetBatchDeliveryReportEndpoint("test_project_id", request_data)
    
    error_response = HTTPResponse(
        status_code=400,
        body=1,
        headers={}
    )
    
    with pytest.raises(SmsException) as exc_info:
        endpoint.handle_response(error_response)
    
    assert str(exc_info.value) == "Error 400"
    assert exc_info.value.http_response == error_response
    assert exc_info.value.is_from_server is True
    assert exc_info.value.response_status_code == 400
