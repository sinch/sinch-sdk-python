from sinch.core.pagination import IntBasedPaginator, AsyncIntBasedPaginator
from sinch.domains.sms.models.groups.responses import SinchListSMSGroupResponse


def test_list_sms_groups(sinch_client_sync):
    list_group_response = sinch_client_sync.sms.groups.list()
    assert isinstance(list_group_response.result, SinchListSMSGroupResponse)


async def test_list_sms_groups_async(sinch_client_async):
    list_group_response = await sinch_client_async.sms.groups.list()
    assert isinstance(list_group_response.result, SinchListSMSGroupResponse)


def test_list_sms_groups_using_pagination(sinch_client_sync):
    list_group_response = sinch_client_sync.sms.groups.list()

    page_counter = 0
    assert list_group_response.result.page == page_counter

    for page in list_group_response.auto_paging_iter():
        page_counter += 1
        assert page.result.page == page_counter
        assert isinstance(page, IntBasedPaginator)


async def test_list_sms_groups_using_pagination_async(sinch_client_async):
    list_group_response = await sinch_client_async.sms.groups.list()

    page_counter = 0
    assert list_group_response.result.page == page_counter

    async for page in list_group_response.auto_paging_iter():
        page_counter += 1
        assert page.result.page == page_counter
        assert isinstance(page, AsyncIntBasedPaginator)
