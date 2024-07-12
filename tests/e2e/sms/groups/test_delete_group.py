from sinch.domains.sms.models.groups.responses import SinchDeleteSMSGroupResponse


def test_delete_sms_group(sinch_client_sync):
    list_group_response = sinch_client_sync.sms.groups.list()

    delete_group_response = sinch_client_sync.sms.groups.delete(
        group_id=list_group_response.result.groups[0].id
    )
    assert isinstance(delete_group_response, SinchDeleteSMSGroupResponse)


def test_delete_sms_group_with_service_plan_id(sinch_client_sync_with_sms_token_authentication):
    list_group_response = sinch_client_sync_with_sms_token_authentication.sms.groups.list()

    delete_group_response = sinch_client_sync_with_sms_token_authentication.sms.groups.delete(
        group_id=list_group_response.result.groups[0].id
    )
    assert isinstance(delete_group_response, SinchDeleteSMSGroupResponse)


async def test_delete_sms_group_async(sinch_client_async):
    list_group_response = await sinch_client_async.sms.groups.list()

    delete_group_response = await sinch_client_async.sms.groups.delete(
        group_id=list_group_response.result.groups[0].id
    )
    assert isinstance(delete_group_response, SinchDeleteSMSGroupResponse)
