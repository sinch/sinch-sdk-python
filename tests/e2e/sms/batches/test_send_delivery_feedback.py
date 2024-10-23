from sinch.domains.sms.models.batches.responses import SendSMSDeliveryFeedbackResponse


def test_send_delivery_feedback(sinch_client_sync, phone_number):
    list_batches_response = sinch_client_sync.sms.batches.list(
        start_date="2019-08-24T14:15:22Z",
        page_size=1
    )
    delivery_feedback_response = sinch_client_sync.sms.batches.send_delivery_feedback(
        batch_id=list_batches_response.result.batches[0].id,
        recipients=[phone_number]
    )
    assert isinstance(delivery_feedback_response, SendSMSDeliveryFeedbackResponse)


def test_send_delivery_feedback_with_service_plan_id(sinch_client_sync_with_sms_token_authentication, phone_number):
    list_batches_response = sinch_client_sync_with_sms_token_authentication.sms.batches.list()
    delivery_feedback_response = sinch_client_sync_with_sms_token_authentication.sms.batches.send_delivery_feedback(
        batch_id=list_batches_response.result.batches[0].id,
        recipients=[phone_number]
    )
    assert isinstance(delivery_feedback_response, SendSMSDeliveryFeedbackResponse)


async def test_send_delivery_feedback_async(sinch_client_async, phone_number):
    list_batches_response = await sinch_client_async.sms.batches.list(
        start_date="2019-08-24T14:15:22Z",
        page_size=1
    )
    delivery_feedback_response = await sinch_client_async.sms.batches.send_delivery_feedback(
        batch_id=list_batches_response.result.batches[0].id,
        recipients=[phone_number]
    )
    assert isinstance(delivery_feedback_response, SendSMSDeliveryFeedbackResponse)
