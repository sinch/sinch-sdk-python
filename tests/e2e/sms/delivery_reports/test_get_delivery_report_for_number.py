from sinch.domains.sms.models.delivery_reports.responses import (
    GetSMSDeliveryReportForNumberResponse,
    ListSMSDeliveryReportsResponse
)


def test_get_delivery_reports_for_specific_number(sinch_client_sync):
    list_delivery_reports_response = sinch_client_sync.sms.delivery_reports.list(
        start_date="2019-08-24T14:15:22Z"
    )
    assert isinstance(list_delivery_reports_response.result, ListSMSDeliveryReportsResponse)

    get_delivery_report_response = sinch_client_sync.sms.delivery_reports.get_for_number(
        batch_id=list_delivery_reports_response.result.delivery_reports[0].batch_id,
        recipient_number=list_delivery_reports_response.result.delivery_reports[0].recipient
    )
    assert isinstance(get_delivery_report_response, GetSMSDeliveryReportForNumberResponse)


def test_get_delivery_reports_for_specific_number_with_service_plan_id(sinch_client_sync_with_sms_token_authentication):
    list_delivery_reports_response = sinch_client_sync_with_sms_token_authentication.sms.delivery_reports.list(
        start_date="2019-08-24T14:15:22Z"
    )
    assert isinstance(list_delivery_reports_response.result, ListSMSDeliveryReportsResponse)

    get_delivery_report_response = sinch_client_sync_with_sms_token_authentication.sms.delivery_reports.get_for_number(
        batch_id=list_delivery_reports_response.result.delivery_reports[0].batch_id,
        recipient_number=list_delivery_reports_response.result.delivery_reports[0].recipient
    )
    assert isinstance(get_delivery_report_response, GetSMSDeliveryReportForNumberResponse)


async def test_get_delivery_reports_for_specific_number_async(sinch_client_async, sinch_client_sync):
    list_delivery_reports_response = sinch_client_sync.sms.delivery_reports.list(
        start_date="2019-08-24T14:15:22Z"
    )
    assert isinstance(list_delivery_reports_response.result, ListSMSDeliveryReportsResponse)

    get_delivery_report_response = await sinch_client_async.sms.delivery_reports.get_for_number(
        batch_id=list_delivery_reports_response.result.delivery_reports[0].batch_id,
        recipient_number=list_delivery_reports_response.result.delivery_reports[0].recipient
    )
    assert isinstance(get_delivery_report_response, GetSMSDeliveryReportForNumberResponse)
