from sinch.domains.sms.models.groups.responses import ReplaceSMSGroupResponse


def test_replace_sms_group(sinch_client_sync):
    list_group_response = sinch_client_sync.sms.groups.list()

    replace_group_response = sinch_client_sync.sms.groups.replace(
        group_id=list_group_response.result.groups[0].id,
        members=["48111111111"]
    )
    assert isinstance(replace_group_response, ReplaceSMSGroupResponse)


async def test_replace_sms_group_async(sinch_client_async):
    list_group_response = await sinch_client_async.sms.groups.list()

    replace_group_response = await sinch_client_async.sms.groups.replace(
        group_id=list_group_response.result.groups[0].id,
        members=["48111111111"]
    )
    assert isinstance(replace_group_response, ReplaceSMSGroupResponse)
