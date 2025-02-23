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


# Helper function to initialize token paginators
def initialize_token_paginator(endpoint_mock, request_data, responses, is_async=False):
    client = AsyncMock() if is_async else Mock()
    client.configuration.transport.request.side_effect = responses

    endpoint_mock.request_data = request_data

    if is_async:
        return AsyncTokenBasedPaginator._initialize(sinch=client, endpoint=endpoint_mock)
    return TokenBasedPaginator(sinch=client, endpoint=endpoint_mock)

EXPECTED_PHONE_NUMBERS = [
    '+12345678901', '+12345678902', '+12345678903', '+12345678904', '+12345678905'
]


def test_page_token_iterator_sync_using_manual_pagination(
        token_based_pagination_request_data,
        mock_pagination_active_number_responses
):
    token_based_paginator = initialize_token_paginator(
        endpoint_mock=Mock(),
        request_data=token_based_pagination_request_data,
        responses=mock_pagination_active_number_responses
    )
    assert token_based_paginator is not None

    page_counter = 1
    active_numbers_list = [num.phone_number for num in token_based_paginator.content()]

    while token_based_paginator.has_next_page:
        token_based_paginator = token_based_paginator.next_page()
        page_counter += 1
        assert isinstance(token_based_paginator, TokenBasedPaginator)
        active_numbers_list.extend(num.phone_number for num in token_based_paginator.content())

    assert page_counter == 3
    assert active_numbers_list == EXPECTED_PHONE_NUMBERS


def test_page_token_iterator_sync_using_auto_pagination(
        token_based_pagination_request_data,
        mock_pagination_active_number_responses
):
    token_based_paginator = initialize_token_paginator(
        endpoint_mock=Mock(),
        request_data=token_based_pagination_request_data,
        responses=mock_pagination_active_number_responses
    )
    assert token_based_paginator is not None

    active_numbers_list = [num.phone_number for num in token_based_paginator.iterator()]

    assert len(active_numbers_list) == len(EXPECTED_PHONE_NUMBERS)
    assert active_numbers_list == EXPECTED_PHONE_NUMBERS


@pytest.mark.asyncio
async def test_page_token_iterator_async_using_manual_pagination(
    token_based_pagination_request_data,
    mock_pagination_active_number_responses
):
    async_token_based_paginator = await initialize_token_paginator(
        endpoint_mock=AsyncMock(),
        request_data=token_based_pagination_request_data,
        responses=mock_pagination_active_number_responses,
        is_async=True
    )
    assert async_token_based_paginator is not None

    active_numbers_list = [num.phone_number for num in async_token_based_paginator.content()]
    page_counter = 1

    while async_token_based_paginator.has_next_page:
        async_token_based_paginator = await async_token_based_paginator.next_page()
        page_counter += 1
        assert isinstance(async_token_based_paginator, AsyncTokenBasedPaginator)
        active_numbers_list.extend(num.phone_number for num in async_token_based_paginator.content())

    assert page_counter == 3
    assert active_numbers_list == EXPECTED_PHONE_NUMBERS


@pytest.mark.asyncio
async def test_page_token_iterator_numbers_async_using_auto_pagination_expects_iter(
    token_based_pagination_request_data,
    mock_pagination_active_number_responses
):
    async_token_based_paginator = await initialize_token_paginator(
        endpoint_mock=AsyncMock(),
        request_data=token_based_pagination_request_data,
        responses=mock_pagination_active_number_responses,
        is_async=True
    )
    assert async_token_based_paginator is not None

    active_numbers_list = [
        num.phone_number async for num in async_token_based_paginator.iterator()
    ]

    assert len(active_numbers_list) == len(EXPECTED_PHONE_NUMBERS)
    assert active_numbers_list == EXPECTED_PHONE_NUMBERS
