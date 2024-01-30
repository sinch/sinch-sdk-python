from sinch.domains.sms.models.batches.responses import ListSMSBatchesResponse
from sinch.core.pagination import IntBasedPaginator, AsyncIntBasedPaginator
from sinch.core.enums import HTTPAuthentication


def test_list_sms_batches(sinch_client_sync):
    list_batches_response = sinch_client_sync.sms.batches.list()
    assert isinstance(list_batches_response, IntBasedPaginator)


def test_list_sms_batches_using_service_plan_id(sinch_client_sync):
    sinch_client_sync.configuration.set_sms_authentication_method(HTTPAuthentication.SMS_TOKEN.value)
    list_batches_response = sinch_client_sync.sms.batches.list()
    assert isinstance(list_batches_response, IntBasedPaginator)


def test_list_sms_batches_with_page_size_1(sinch_client_sync):
    list_batches_response = sinch_client_sync.sms.batches.list(
        page_size=1,
    )
    assert isinstance(list_batches_response.result, ListSMSBatchesResponse)
    assert len(list_batches_response.result.batches) == 1


def test_list_sms_batches_with_start_date(sinch_client_sync):
    list_batches_response = sinch_client_sync.sms.batches.list(
        page_size=2,
        start_date="2022-05-17T21:37:00.051Z"
    )
    assert isinstance(list_batches_response.result, ListSMSBatchesResponse)


def test_list_sms_batches_using_manual_pagination(sinch_client_sync):
    list_batches_response = sinch_client_sync.sms.batches.list(
        start_date="2019-08-24T14:15:22Z",
        page_size=1
    )

    # Page iteration starts from 0...
    page_counter = 0
    assert list_batches_response.result.page == page_counter

    while list_batches_response.has_next_page:
        list_batches_response = list_batches_response.next_page()
        page_counter += 1
        assert list_batches_response.result.page == page_counter


def test_list_sms_batches_using_auto_pagination(sinch_client_sync):
    list_batches_response = sinch_client_sync.sms.batches.list(
        page_size=1,
        start_date="2019-08-24T14:15:22Z"
    )

    page_counter = 0
    assert list_batches_response.result.page == page_counter

    for page in list_batches_response.auto_paging_iter():
        page_counter += 1
        assert page.result.page == page_counter
        assert isinstance(page, IntBasedPaginator)


async def test_list_sms_batches_using_manual_pagination_async(sinch_client_async):
    list_batches_response = await sinch_client_async.sms.batches.list(
        start_date="2019-08-24T14:15:22Z",
        page_size=1
    )
    page_counter = 1

    while list_batches_response.has_next_page:
        list_batches_response = await list_batches_response.next_page()
        assert isinstance(list_batches_response, AsyncIntBasedPaginator)
        page_counter += 1

    assert page_counter > 1


async def test_list_sms_batches_using_auto_pagination_async(sinch_client_async):
    list_batches_response = await sinch_client_async.sms.batches.list(
        start_date="2019-08-24T14:15:22Z",
        page_size=1
    )
    page_counter = 1

    async for page in list_batches_response.auto_paging_iter():
        assert isinstance(page, AsyncIntBasedPaginator)
        page_counter += 1

    assert page_counter > 1
