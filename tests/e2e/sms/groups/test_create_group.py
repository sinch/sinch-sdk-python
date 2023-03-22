from sinch.domains.sms.models.groups.responses import CreateSMSGroupResponse


def test_create_sms_group(sinch_client_sync, phone_number):
    create_group_response = sinch_client_sync.sms.groups.create(
        name="KillerRabbit",
        members=[phone_number]
    )
    assert isinstance(create_group_response, CreateSMSGroupResponse)


async def test_create_sms_group_async_using_child_groups(sinch_client_async, phone_number):
    create_group_response = await sinch_client_async.sms.groups.create(
        name="KillerRabbit2",
        members=[phone_number]
    )
    assert isinstance(create_group_response, CreateSMSGroupResponse)

    create_group_response_with_child_groups = await sinch_client_async.sms.groups.create(
        name="WithChildGroups",
        members=[phone_number],
        child_groups=[create_group_response.id]
    )
    assert isinstance(create_group_response_with_child_groups, CreateSMSGroupResponse)
