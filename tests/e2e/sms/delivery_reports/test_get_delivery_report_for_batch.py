from sinch.core.enums import HTTPAuthentication
from sinch.domains.sms.models.delivery_reports.responses import GetSMSDeliveryReportForBatchResponse


def test_get_delivery_reports_for_specific_batch(sinch_client_sync, phone_number, origin_phone_number):
    send_batch_response = sinch_client_sync.sms.batches.send(
        delivery_report="summary",
        to=[phone_number],
        from_=origin_phone_number,
        body="Delivery report test.",
        feedback_enabled=True,
        callback_url="http://testcallback.pl"
    )
    get_delivery_report_response = sinch_client_sync.sms.delivery_reports.get_for_batch(
        batch_id=send_batch_response.id,
        type_="summary",
        status=["Queued", "Dispatched", "Delivered"],
        code=[400, 405]
    )
    assert isinstance(get_delivery_report_response, GetSMSDeliveryReportForBatchResponse)


def test_get_delivery_reports_for_specific_batch_with_service_plan_id(
    sinch_client_sync,
    phone_number,
    origin_phone_number
):
    sinch_client_sync.configuration.sms_authentication_method = HTTPAuthentication.SMS_TOKEN.value
    send_batch_response = sinch_client_sync.sms.batches.send(
        delivery_report="summary",
        to=[phone_number],
        from_=origin_phone_number,
        body="Delivery report test.",
        feedback_enabled=True,
        callback_url="http://testcallback.pl"
    )
    get_delivery_report_response = sinch_client_sync.sms.delivery_reports.get_for_batch(
        batch_id=send_batch_response.id,
        type_="summary",
        status=["Queued"],
        code=[400]
    )
    assert isinstance(get_delivery_report_response, GetSMSDeliveryReportForBatchResponse)


async def test_get_delivery_reports_for_specific_batch_async(sinch_client_async, phone_number, origin_phone_number):
    send_batch_response = await sinch_client_async.sms.batches.send(
        delivery_report="summary",
        to=[phone_number],
        from_=origin_phone_number,
        body="Delivery report test.",
        feedback_enabled=True,
        callback_url="http://testcallback.pl"
    )
    get_delivery_report_response = await sinch_client_async.sms.delivery_reports.get_for_batch(
        batch_id=send_batch_response.id,
        type_="summary",
        status=["Queued", "Dispatched", "Delivered"],
        code=[400, 405]
    )
    assert isinstance(get_delivery_report_response, GetSMSDeliveryReportForBatchResponse)
