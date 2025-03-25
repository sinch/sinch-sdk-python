import pytest
from unittest.mock import Mock, AsyncMock
from sinch.core.pagination import (
    IntBasedPaginator,
    AsyncIntBasedPaginator,
    TokenBasedPaginator,
    AsyncTokenBasedPaginator
)


def test_page_int_iterator_sync_using_manual_pagination(
    first_int_based_pagination_response,
    second_int_based_pagination_response,
    third_int_based_pagination_response,
    int_based_pagination_request_data
):
    endpoint = Mock()
    endpoint.request_data = int_based_pagination_request_data
    sinch_client = Mock()

    sinch_client.configuration.transport.request.side_effect = [
        first_int_based_pagination_response,
        second_int_based_pagination_response,
        third_int_based_pagination_response
    ]
    int_based_paginator = IntBasedPaginator._initialize(
        sinch=sinch_client,
        endpoint=endpoint
    )
    assert int_based_paginator

    page_counter = 0
    assert int_based_paginator.result.page == page_counter

    while int_based_paginator.has_next_page:
        int_based_paginator = int_based_paginator.next_page()
        page_counter += 1
        assert int_based_paginator.result.page == page_counter

    assert page_counter == 2


def test_page_int_iterator_sync_using_auto_pagination(
    first_int_based_pagination_response,
    second_int_based_pagination_response,
    third_int_based_pagination_response,
    int_based_pagination_request_data
):
    endpoint = Mock()
    endpoint.request_data = int_based_pagination_request_data
    sinch_client = Mock()

    sinch_client.configuration.transport.request.side_effect = [
        first_int_based_pagination_response,
        second_int_based_pagination_response,
        third_int_based_pagination_response
    ]

    int_based_paginator = IntBasedPaginator._initialize(
        sinch=sinch_client,
        endpoint=endpoint
    )
    assert int_based_paginator

    page_counter = 0
    assert int_based_paginator.result.page == page_counter

    for page in int_based_paginator.auto_paging_iter():
        page_counter += 1
        assert page.result.page == page_counter
        assert isinstance(page, IntBasedPaginator)

    assert page_counter == 2


async def test_page_int_iterator_async_using_manual_pagination(
    first_int_based_pagination_response,
    second_int_based_pagination_response,
    third_int_based_pagination_response,
    int_based_pagination_request_data
):
    endpoint = Mock()
    endpoint.request_data = int_based_pagination_request_data
    sinch_client = AsyncMock()

    sinch_client.configuration.transport.request.side_effect = [
        first_int_based_pagination_response,
        second_int_based_pagination_response,
        third_int_based_pagination_response
    ]
    int_based_paginator = await AsyncIntBasedPaginator._initialize(
        sinch=sinch_client,
        endpoint=endpoint
    )
    assert int_based_paginator

    page_counter = 0
    assert int_based_paginator.result.page == page_counter

    while int_based_paginator.has_next_page:
        int_based_paginator = await int_based_paginator.next_page()
        page_counter += 1
        assert int_based_paginator.result.page == page_counter

    assert page_counter == 2


async def test_page_int_iterator_async_using_auto_pagination(
    first_int_based_pagination_response,
    second_int_based_pagination_response,
    third_int_based_pagination_response,
    int_based_pagination_request_data
):
    endpoint = Mock()
    endpoint.request_data = int_based_pagination_request_data
    sinch_client = AsyncMock()

    sinch_client.configuration.transport.request.side_effect = [
        first_int_based_pagination_response,
        second_int_based_pagination_response,
        third_int_based_pagination_response
    ]

    int_based_paginator = await AsyncIntBasedPaginator._initialize(
        sinch=sinch_client,
        endpoint=endpoint
    )
    assert int_based_paginator

    page_counter = 0
    assert int_based_paginator.result.page == page_counter

    async for page in int_based_paginator.auto_paging_iter():
        page_counter += 1
        assert isinstance(page, AsyncIntBasedPaginator)

    assert page_counter == 3
    assert not int_based_paginator.result.pig_dogs


# Helper function to initialize token paginator
def initialize_token_paginator(endpoint_mock, request_data, responses, is_async=False):
    client = AsyncMock() if is_async else Mock()
    client.configuration.transport.request.side_effect = responses

    endpoint_mock.request_data = request_data

    if is_async:
        return AsyncTokenBasedPaginator._initialize(sinch=client, endpoint=endpoint_mock)
    return TokenBasedPaginator(sinch=client, endpoint=endpoint_mock)


def test_page_token_iterator_sync_using_manual_pagination(
    token_based_pagination_request_data,
    mock_pagination_active_number_responses,
    mock_pagination_expected_phone_numbers_response
):
    """ Test that the pagination iterates correctly through multiple items. """
    token_based_paginator = initialize_token_paginator(
        endpoint_mock=Mock(),
        request_data=token_based_pagination_request_data,
        responses=mock_pagination_active_number_responses
    )
    assert token_based_paginator is not None

    page_counter = 1
    active_numbers_list = []
    reached_last_page = False
    while not reached_last_page:
        active_numbers_list.extend([num.phone_number for num in token_based_paginator.content()])
        if token_based_paginator.has_next_page:
            token_based_paginator = token_based_paginator.next_page()
            page_counter += 1
            assert isinstance(token_based_paginator, TokenBasedPaginator)
        else:
            reached_last_page = True

    assert page_counter == 3
    assert active_numbers_list == mock_pagination_expected_phone_numbers_response


def test_page_token_iterator_sync_using_auto_pagination_expects_iter(
    token_based_pagination_request_data,
    mock_pagination_active_number_responses,
    mock_pagination_expected_phone_numbers_response
):
    """Test that the pagination iterates correctly through multiple items."""
    token_based_paginator = initialize_token_paginator(
            endpoint_mock=Mock(),
            request_data=token_based_pagination_request_data,
            responses=mock_pagination_active_number_responses
    )
    assert token_based_paginator is not None

    active_numbers_list = []
    for number in token_based_paginator.iterator():
        active_numbers_list.append(number.phone_number)

    assert len(active_numbers_list) == len(mock_pagination_expected_phone_numbers_response)
    assert active_numbers_list == mock_pagination_expected_phone_numbers_response


@pytest.mark.asyncio
async def test_page_token_iterator_async_using_manual_pagination_expects_iter(
    token_based_pagination_request_data,
    mock_pagination_active_number_responses,
    mock_pagination_expected_phone_numbers_response
):
    """Test that the async pagination iterates correctly through multiple items."""
    async_token_based_paginator = await initialize_token_paginator(
        endpoint_mock=AsyncMock(),
        request_data=token_based_pagination_request_data,
        responses=mock_pagination_active_number_responses,
        is_async=True
    )
    assert async_token_based_paginator is not None

    active_numbers_list = []
    page_counter = 1
    reached_last_page = False
    while not reached_last_page:
        active_numbers_list.extend([num.phone_number for num in async_token_based_paginator.content()])
        if async_token_based_paginator.has_next_page:
            async_token_based_paginator = await async_token_based_paginator.next_page()
            page_counter += 1
            assert isinstance(async_token_based_paginator, AsyncTokenBasedPaginator)
        else:
            reached_last_page = True

    assert page_counter == 3
    assert active_numbers_list == mock_pagination_expected_phone_numbers_response


@pytest.mark.asyncio
async def test_page_token_iterator_async_using_auto_pagination_expects_iter(
    token_based_pagination_request_data,
    mock_pagination_active_number_responses,
    mock_pagination_expected_phone_numbers_response
):
    """Test that the async pagination iterates correctly through multiple items."""
    async_token_based_paginator = await initialize_token_paginator(
        endpoint_mock=AsyncMock(),
        request_data=token_based_pagination_request_data,
        responses=mock_pagination_active_number_responses,
        is_async=True
    )
    assert async_token_based_paginator is not None

    active_numbers_list = []
    async for number in async_token_based_paginator.iterator():
        active_numbers_list.append(number.phone_number)

    assert len(active_numbers_list) == len(mock_pagination_expected_phone_numbers_response)
    assert active_numbers_list == mock_pagination_expected_phone_numbers_response
