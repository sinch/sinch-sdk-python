from sinch.domains.numbers import ListActiveNumbersResponse, UpdateNumberConfigurationResponse, \
    GetNumberConfigurationResponse, ReleaseNumberFromProjectResponse

from sinch.core.pagination import TokenBasedPaginator, AsyncTokenBasedPaginator


def get_active_numbers_for_project(sinch_client_sync):
    active_numbers_response = sinch_client_sync.numbers.active.list(
        region_code="GB",
        number_type="MOBILE"
    )
    assert isinstance(active_numbers_response.result, ListActiveNumbersResponse)
    return active_numbers_response


def test_list_active_numbers(sinch_client_sync):
    active_numbers_response = get_active_numbers_for_project(
        sinch_client_sync
    )
    assert len(active_numbers_response.result.active_numbers) > 0


def test_list_active_numbers_limit_page_size(sinch_client_sync):
    active_numbers_response = sinch_client_sync.numbers.active.list(
        region_code="GB",
        number_type="MOBILE",
        page_size=1
    )
    assert len(active_numbers_response.result.active_numbers) == 1
    assert isinstance(active_numbers_response.result, ListActiveNumbersResponse)


def test_list_active_numbers_using_manual_pagination(sinch_client_sync):
    active_numbers_response = sinch_client_sync.numbers.active.list(
        region_code="GB",
        number_type="MOBILE",
        page_size=1
    )
    page_counter = 1

    while active_numbers_response.has_next_page:
        active_numbers_response = active_numbers_response.next_page()
        page_counter += 1

    assert page_counter > 1


def test_list_active_numbers_using_auto_pagination(sinch_client_sync):
    active_numbers_response = sinch_client_sync.numbers.active.list(
        region_code="GB",
        number_type="MOBILE",
        page_size=1
    )
    page_counter = 1

    for page in active_numbers_response.auto_paging_iter():
        assert isinstance(page, TokenBasedPaginator)
        page_counter += 1

    assert page_counter > 1


def test_list_active_numbers_using_number_pattern(sinch_client_sync):
    active_numbers_response = sinch_client_sync.numbers.active.list(
        region_code="GB",
        number_type="MOBILE",
        number_pattern="626",
        number_search_pattern="END"
    )
    assert "626" in active_numbers_response.result.active_numbers[0].phone_number


async def test_list_active_numbers_using_manual_pagination_async(sinch_client_async):
    active_numbers_response = await sinch_client_async.numbers.active.list(
        region_code="GB",
        number_type="MOBILE",
        page_size=1
    )
    page_counter = 1

    while active_numbers_response.has_next_page:
        active_numbers_response = await active_numbers_response.next_page()
        page_counter += 1

    assert isinstance(active_numbers_response, AsyncTokenBasedPaginator)
    assert page_counter > 1


async def test_list_active_numbers_using_auto_pagination_async(sinch_client_async):
    active_numbers_response = await sinch_client_async.numbers.active.list(
        region_code="GB",
        number_type="MOBILE",
        page_size=1
    )
    page_counter = 1

    async for page in active_numbers_response.auto_paging_iter():
        assert isinstance(page, AsyncTokenBasedPaginator)
        page_counter += 1

    assert page_counter > 1


def test_get_phone_number_configuration(sinch_client_sync):
    active_numbers_response = get_active_numbers_for_project(sinch_client_sync)
    get_configuration_response = sinch_client_sync.numbers.active.get(
        active_numbers_response.result.active_numbers[0].phone_number
    )
    assert isinstance(get_configuration_response, GetNumberConfigurationResponse)


def test_update_phone_number_configuration(sinch_client_sync):
    active_numbers_response = get_active_numbers_for_project(sinch_client_sync)
    update_number_response = sinch_client_sync.numbers.active.update(
        active_numbers_response.result.active_numbers[0].phone_number,
        display_name="test_success!"
    )
    assert isinstance(update_number_response, UpdateNumberConfigurationResponse)


def test_release_number_from_project(sinch_client_sync):
    active_numbers_response = get_active_numbers_for_project(sinch_client_sync)
    release_number_response = sinch_client_sync.numbers.active.release(
        active_numbers_response.result.active_numbers[0].phone_number,
    )
    assert isinstance(release_number_response, ReleaseNumberFromProjectResponse)
