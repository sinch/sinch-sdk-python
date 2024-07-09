from sinch.domains.sms.models.groups.responses import UpdateSMSGroupResponse
from sinch.core.enums import HTTPAuthentication


def test_update_sms_group(sinch_client_sync, phone_number):
    list_group_response = sinch_client_sync.sms.groups.list()

    update_group_response = sinch_client_sync.sms.groups.update(
        name="KillerRabbit222",
        group_id=list_group_response.result.groups[0].id
    )
    assert isinstance(update_group_response, UpdateSMSGroupResponse)
    assert update_group_response.name == "KillerRabbit222"



def test_add_phone_number_to_sms_group(sinch_client_sync, phone_number):
    list_group_response = sinch_client_sync.sms.groups.list()

    update_group_response = sinch_client_sync.sms.groups.update(
        group_id=list_group_response.result.groups[20].id,
        add=["+48111222333"]
    )
    assert isinstance(update_group_response, UpdateSMSGroupResponse)


async def test_update_sms_group_async(sinch_client_async):
    list_group_response = await sinch_client_async.sms.groups.list()

    update_group_response = await sinch_client_async.sms.groups.update(
        name="KillerRabbit333",
        group_id=list_group_response.result.groups[0].id
    )
    assert isinstance(update_group_response, UpdateSMSGroupResponse)
    assert update_group_response.name == "KillerRabbit333"
