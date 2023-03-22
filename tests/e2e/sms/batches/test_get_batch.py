from sinch.domains.sms.models.batches.responses import GetSMSBatchResponse


def test_get_sms_batch(sinch_client_sync):
    list_batch_response = sinch_client_sync.sms.batches.list()
    get_batch_response = sinch_client_sync.sms.batches.get(
        batch_id=list_batch_response.result.batches[0].id
    )
    assert isinstance(get_batch_response, GetSMSBatchResponse)


async def test_get_sms_batch_async(sinch_client_async):
    list_batch_response = await sinch_client_async.sms.batches.list()
    get_batch_response = await sinch_client_async.sms.batches.get(
        batch_id=list_batch_response.result.batches[0].id
    )
    assert isinstance(get_batch_response, GetSMSBatchResponse)
