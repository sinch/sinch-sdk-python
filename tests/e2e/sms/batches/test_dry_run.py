from sinch.domains.sms.models.batches.responses import SendSMSBatchDryRunResponse


def test_send_sms_dry_run(sinch_client_sync, phone_number, origin_phone_number):
    send_dry_run_response = sinch_client_sync.sms.batches.send_dry_run(
        number_of_recipients=10,
        per_recipient=True,
        to=[phone_number],
        from_=origin_phone_number,
        body="Spanish Inquisition"
    )
    assert isinstance(send_dry_run_response, SendSMSBatchDryRunResponse)


def test_send_sms_dry_run_with_service_plan_id(
    sinch_client_sync_with_sms_token_authentication,
    phone_number,
    origin_phone_number
):
    send_dry_run_response = sinch_client_sync_with_sms_token_authentication.sms.batches.send_dry_run(
        number_of_recipients=10,
        per_recipient=True,
        to=[phone_number],
        from_=origin_phone_number,
        body="Spanish Inquisition"
    )
    assert isinstance(send_dry_run_response, SendSMSBatchDryRunResponse)


async def test_send_sms_dry_run_async(sinch_client_async, phone_number, origin_phone_number):
    send_dry_run_response = await sinch_client_async.sms.batches.send_dry_run(
        number_of_recipients=10,
        per_recipient=True,
        to=[phone_number],
        from_=origin_phone_number,
        body="Spanish Inquisition"
    )
    assert isinstance(send_dry_run_response, SendSMSBatchDryRunResponse)
