from sinch.domains.sms.models.batches.responses import UpdateSMSBatchResponse


def test_update_sms_batch(sinch_client_sync, phone_number, origin_phone_number):
    send_batch_response = sinch_client_sync.sms.batches.send(
        delivery_report="none",
        to=[phone_number],
        from_=origin_phone_number,
        body="Update Batch Test",
        feedback_enabled=True,
        send_at="2022-12-01T21:37:00Z"
    )
    update_batch_response = sinch_client_sync.sms.batches.update(
        batch_id=send_batch_response.id,
        body="Update Batch Test After Update"
    )
    assert isinstance(update_batch_response, UpdateSMSBatchResponse)
    assert update_batch_response.body == "Update Batch Test After Update"


async def test_update_sms_batch_async(sinch_client_async, phone_number, origin_phone_number):
    send_batch_response = await sinch_client_async.sms.batches.send(
        delivery_report="none",
        to=[phone_number],
        from_=origin_phone_number,
        body="Update Batch Test",
        feedback_enabled=True,
        send_at="2022-12-01T21:37:00Z"
    )
    update_batch_response = await sinch_client_async.sms.batches.update(
        batch_id=send_batch_response.id,
        body="Update Batch Test After Update"
    )
    assert isinstance(update_batch_response, UpdateSMSBatchResponse)
    assert update_batch_response.body == "Update Batch Test After Update"
