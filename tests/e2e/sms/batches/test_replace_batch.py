from sinch.domains.sms.models.batches.responses import ReplaceSMSBatchResponse


def test_replace_sms_batch(sinch_client_sync, phone_number):
    list_batches_response = sinch_client_sync.sms.batches.list(
        start_date="2022-11-24T14:15:22Z"
    )
    replace_batch_response = sinch_client_sync.sms.batches.replace(
        batch_id=list_batches_response.result.batches[15].id,
        to=[phone_number],
        body="Replace SMS batch test"
    )
    assert isinstance(replace_batch_response, ReplaceSMSBatchResponse)


def test_replace_sms_batch_with_service_plan_id(
    sinch_client_sync_with_sms_token_authentication,
    phone_number
):
    list_batches_response = sinch_client_sync_with_sms_token_authentication.sms.batches.list(
        start_date="2022-11-24T14:15:22Z"
    )
    replace_batch_response = sinch_client_sync_with_sms_token_authentication.sms.batches.replace(
        batch_id=list_batches_response.result.batches[0].id,
        to=[phone_number],
        body="Replace SMS batch test"
    )
    assert isinstance(replace_batch_response, ReplaceSMSBatchResponse)


async def test_replace_sms_batch_async(sinch_client_async, sinch_client_sync, phone_number):
    list_batches_response = sinch_client_sync.sms.batches.list(
        start_date="2022-11-24T14:15:22Z"
    )
    replace_batch_response = await sinch_client_async.sms.batches.replace(
        batch_id=list_batches_response.result.batches[15].id,
        to=[phone_number],
        body="Replace SMS batch test"
    )
    assert isinstance(replace_batch_response, ReplaceSMSBatchResponse)
