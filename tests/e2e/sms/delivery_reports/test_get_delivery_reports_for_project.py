from sinch.domains.sms.models.delivery_reports.responses import ListSMSDeliveryReportsResponse


def test_get_delivery_reports_for_project(sinch_client_sync):
    list_delivery_reports_response = sinch_client_sync.sms.delivery_reports.list(
        start_date="2019-08-24T14:15:22Z"
    )
    assert isinstance(list_delivery_reports_response.result, ListSMSDeliveryReportsResponse)


def test_get_delivery_reports_for_project_with_service_plan_id(sinch_client_sync_with_sms_token_authentication):
    list_delivery_reports_response = sinch_client_sync_with_sms_token_authentication.sms.delivery_reports.list(
        start_date="2019-08-24T14:15:22Z"
    )
    assert isinstance(list_delivery_reports_response.result, ListSMSDeliveryReportsResponse)


async def test_get_delivery_reports_for_project_async(sinch_client_async):
    list_delivery_reports_response = await sinch_client_async.sms.delivery_reports.list()
    assert isinstance(list_delivery_reports_response.result, ListSMSDeliveryReportsResponse)
