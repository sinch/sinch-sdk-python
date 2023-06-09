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

    page_counter = 0
    async for page in int_based_paginator.auto_paging_iter():
        page_counter += 1
        assert isinstance(page, AsyncIntBasedPaginator)

    assert page_counter == 2
    assert not int_based_paginator.result.pig_dogs


def test_page_token_iterator_sync_using_manual_pagination(
    token_based_pagination_request_data,
    first_token_based_pagination_response,
    second_token_based_pagination_response
):
    endpoint = Mock()
    endpoint.request_data = token_based_pagination_request_data
    sinch_client = Mock()

    sinch_client.configuration.transport.request.side_effect = [
        first_token_based_pagination_response,
        second_token_based_pagination_response
    ]
    token_based_paginator = TokenBasedPaginator._initialize(
        sinch=sinch_client,
        endpoint=endpoint
    )
    assert token_based_paginator

    page_counter = 0
    while token_based_paginator.has_next_page:
        token_based_paginator = token_based_paginator.next_page()
        page_counter += 1
        assert isinstance(token_based_paginator, TokenBasedPaginator)

    assert page_counter == 1


def test_page_token_iterator_sync_using_auto_pagination(
    token_based_pagination_request_data,
    first_token_based_pagination_response,
    second_token_based_pagination_response
):
    endpoint = Mock()
    endpoint.request_data = token_based_pagination_request_data
    sinch_client = Mock()

    sinch_client.configuration.transport.request.side_effect = [
        first_token_based_pagination_response,
        second_token_based_pagination_response
    ]
    token_based_paginator = TokenBasedPaginator._initialize(
        sinch=sinch_client,
        endpoint=endpoint
    )
    assert token_based_paginator

    page_counter = 0
    for page in token_based_paginator.auto_paging_iter():
        page_counter += 1
        assert isinstance(page, TokenBasedPaginator)

    assert page_counter == 1


async def test_page_token_iterator_async_using_manual_pagination(
    token_based_pagination_request_data,
    first_token_based_pagination_response,
    second_token_based_pagination_response
):
    endpoint = Mock()
    endpoint.request_data = token_based_pagination_request_data
    sinch_client = AsyncMock()

    sinch_client.configuration.transport.request.side_effect = [
        first_token_based_pagination_response,
        second_token_based_pagination_response
    ]
    token_based_paginator = await AsyncTokenBasedPaginator._initialize(
        sinch=sinch_client,
        endpoint=endpoint
    )
    assert token_based_paginator

    page_counter = 0
    while token_based_paginator.has_next_page:
        token_based_paginator = await token_based_paginator.next_page()
        page_counter += 1
        assert isinstance(token_based_paginator, AsyncTokenBasedPaginator)

    assert page_counter == 1


async def test_page_token_iterator_async_using_auto_pagination(
    token_based_pagination_request_data,
    first_token_based_pagination_response,
    second_token_based_pagination_response
):
    endpoint = Mock()
    endpoint.request_data = token_based_pagination_request_data
    sinch_client = AsyncMock()

    sinch_client.configuration.transport.request.side_effect = [
        first_token_based_pagination_response,
        second_token_based_pagination_response
    ]
    token_based_paginator = await AsyncTokenBasedPaginator._initialize(
        sinch=sinch_client,
        endpoint=endpoint
    )
    assert token_based_paginator

    page_counter = 0
    async for page in token_based_paginator.auto_paging_iter():
        page_counter += 1
        assert isinstance(page, AsyncTokenBasedPaginator)

    assert page_counter == 1
