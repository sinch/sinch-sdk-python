from sinch.domains.sms.models.inbounds.responses import SinchListInboundMessagesResponse


def test_list_inbound_sms(sinch_client_sync):
    list_incoming_message_response = sinch_client_sync.sms.inbounds.list()
    assert isinstance(list_incoming_message_response.result, SinchListInboundMessagesResponse)


def test_list_inbound_sms_with_service_plan_id(sinch_client_sync_with_service_plan_id):
    list_incoming_message_response = sinch_client_sync_with_service_plan_id.sms.inbounds.list()
    assert isinstance(list_incoming_message_response.result, SinchListInboundMessagesResponse)


async def test_list_inbound_sms_async(sinch_client_async):
    list_incoming_message_response = await sinch_client_async.sms.inbounds.list()
    assert isinstance(list_incoming_message_response.result, SinchListInboundMessagesResponse)
