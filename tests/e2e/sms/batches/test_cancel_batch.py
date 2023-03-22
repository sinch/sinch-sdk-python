from sinch.domains.sms.models.batches.responses import CancelSMSBatchResponse


def test_cancel_sms_batch(sinch_client_sync, phone_number, origin_phone_number):
    send_batch_response = sinch_client_sync.sms.batches.send(
        delivery_report="none",
        to=[phone_number],
        from_=origin_phone_number,
        body="Synchronous Batch Cancel",
        feedback_enabled=True,
        send_at="2023-08-24T21:37:00Z"
    )
    cancel_batch_response = sinch_client_sync.sms.batches.cancel(
        batch_id=send_batch_response.id
    )
    assert isinstance(cancel_batch_response, CancelSMSBatchResponse)


async def test_cancel_sms_batch_async(sinch_client_async, phone_number, origin_phone_number):
    send_batch_response = await sinch_client_async.sms.batches.send(
        delivery_report="none",
        to=[phone_number],
        from_=origin_phone_number,
        body="Synchronous Batch Cancel",
        feedback_enabled=True,
        send_at="2023-08-24T21:37:00Z"
    )
    cancel_batch_response = await sinch_client_async.sms.batches.cancel(
        batch_id=send_batch_response.id
    )
    assert isinstance(cancel_batch_response, CancelSMSBatchResponse)
