import pytest
from sinch.domains.sms.models.inbounds.responses import GetInboundMessagesResponse


@pytest.mark.skip(reason="More advanced testing setup required.")  # TODO: fix that
def test_get_inbound_sms(sinch_client_sync):
    list_incoming_message_response = sinch_client_sync.sms.inbounds.list()
    get_incoming_message_response = sinch_client_sync.sms.inbounds.get(
        inbound_id=list_incoming_message_response.result.inbounds[0].id
    )
    assert isinstance(get_incoming_message_response, GetInboundMessagesResponse)


@pytest.mark.skip(reason="More advanced testing setup required.")  # TODO: fix that
async def test_get_inbound_sms_async(sinch_client_async):
    list_incoming_message_response = await sinch_client_async.sms.inbounds.list()
    get_incoming_message_response = await sinch_client_async.sms.inbounds.get(
        inbound_id=list_incoming_message_response.result.inbounds[0].id
    )
    assert isinstance(get_incoming_message_response, GetInboundMessagesResponse)
