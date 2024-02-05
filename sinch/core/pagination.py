from abc import ABC, abstractmethod
from sinch.core.endpoint import HTTPEndpoint
from typing import TYPE_CHECKING, Union, cast, Coroutine, Any
from sinch.core.models.base_model import SinchBaseModel
from sinch.core.models.pagination import (
    TokenPaginatedRequest,
    TokenPaginatedResponse,
    IntPaginatedRequest,
    IntPaginatedResponse
)


if TYPE_CHECKING:
    from sinch.core.clients.sinch_client_base import ClientBase


class Paginator(ABC):
    """
    Pagination response object.

    auto_paging_iter method returns an iterator object that can be used for iterator-based page traversing.
    For example:
        for page in paginated_response.auto_paging_iter():
            ...process page object

    For manual pagination use has_next_page property with next_page() method.
    For example:
        if paginated_response.has_next_page:
            paginated_response = paginated_response.next_page()
    """
    def __init__(
        self,
        sinch: 'ClientBase',
        endpoint: HTTPEndpoint,
        result: Union[TokenPaginatedResponse, IntPaginatedResponse]
    ):
        self._sinch = sinch
        self.result = result
        self.endpoint = endpoint
        self.has_next_page = False
        self._calculate_next_page()

    def __repr__(self) -> str:
        return "Paginated response content: " + str(self.result)

    @abstractmethod
    def auto_paging_iter(self) -> Union['PageIterator', 'AsyncPageIterator']:
        pass

    @abstractmethod
    def next_page(self) -> Union['Paginator', Coroutine[Any, Any, 'Paginator']]:
        pass

    @abstractmethod
    def _calculate_next_page(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def _initialize(
        cls,
        sinch: 'ClientBase',
        endpoint: HTTPEndpoint
    ) -> Union['Paginator', Coroutine[Any, Any, 'Paginator']]:
        pass


class PageIterator:
    def __init__(self, paginator: Paginator):
        self.paginator = paginator

    def __iter__(self) -> 'PageIterator':
        return self

    def __next__(self) -> Paginator:
        if self.paginator.has_next_page:
            return cast(
                Paginator,
                self.paginator.next_page()
            )
        else:
            raise StopIteration


class AsyncPageIterator:
    def __init__(self, paginator: Paginator):
        self.paginator = paginator

    def __aiter__(self) -> 'AsyncPageIterator':
        return self

    async def __anext__(self) -> Paginator:
        if self.paginator.has_next_page:
            return await cast(
                Coroutine[Any, Any, Paginator],
                self.paginator.next_page()
            )
        else:
            raise StopAsyncIteration


class IntBasedPaginator(Paginator):
    result: IntPaginatedResponse
    __doc__ = Paginator.__doc__

    def _calculate_next_page(self) -> None:
        if self.result.page_size:
            self.has_next_page = True
        else:
            self.has_next_page = False

    def next_page(self) -> Union['Paginator', Coroutine[Any, Any, 'Paginator']]:
        cast(IntPaginatedRequest, self.endpoint.request_data).page += 1
        self.result = cast(
            IntPaginatedResponse,
            self._sinch.configuration.transport.request(self.endpoint)
        )
        self._calculate_next_page()
        return self

    def auto_paging_iter(self) -> Union['PageIterator', 'AsyncPageIterator']:
        return PageIterator(self)

    @classmethod
    def _initialize(
        cls,
        sinch: 'ClientBase',
        endpoint: HTTPEndpoint
    ) -> Union['Paginator', Coroutine[Any, Any, 'Paginator']]:

        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, cast(IntPaginatedResponse, result))


class AsyncIntBasedPaginator(IntBasedPaginator):
    __doc__ = IntBasedPaginator.__doc__
    result: IntPaginatedResponse

    async def next_page(self) -> 'Paginator':
        cast(IntPaginatedRequest, self.endpoint.request_data).page += 1
        self.result = await cast(
            Coroutine[Any, Any, IntPaginatedResponse],
            self._sinch.configuration.transport.request(self.endpoint)
        )
        self._calculate_next_page()
        return self

    def auto_paging_iter(self) -> AsyncPageIterator:
        return AsyncPageIterator(self)

    @classmethod
    async def _initialize(cls, sinch: 'ClientBase', endpoint: HTTPEndpoint) -> 'Paginator':
        result = await cast(
            Coroutine[Any, Any, IntPaginatedResponse],
            sinch.configuration.transport.request(endpoint)
        )
        return cls(sinch, endpoint, result)


class TokenBasedPaginator(Paginator):
    __doc__ = Paginator.__doc__
    result: TokenPaginatedResponse

    def _calculate_next_page(self) -> None:
        if self.result.next_page_token:
            self.has_next_page = True
        else:
            self.has_next_page = False

    def next_page(self) -> Union['TokenBasedPaginator', Coroutine[Any, Any, 'AsyncTokenBasedPaginator']]:
        cast(TokenPaginatedRequest, self.endpoint.request_data).page_token = self.result.next_page_token
        self.result = cast(TokenPaginatedResponse, self._sinch.configuration.transport.request(self.endpoint))
        self._calculate_next_page()
        return self

    def auto_paging_iter(self) -> Union[PageIterator, AsyncPageIterator]:
        return PageIterator(self)

    @classmethod
    def _initialize(
        cls,
        sinch: 'ClientBase',
        endpoint: HTTPEndpoint
    ) -> Union['Paginator', Coroutine[Any, Any, 'Paginator']]:

        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, cast(TokenPaginatedResponse, result))


class AsyncTokenBasedPaginator(TokenBasedPaginator):
    __doc__ = TokenBasedPaginator.__doc__
    result: TokenPaginatedResponse

    async def next_page(self) -> 'AsyncTokenBasedPaginator':
        cast(TokenPaginatedRequest, self.endpoint.request_data).page_token = self.result.next_page_token
        self.result = await cast(
            Coroutine[Any, Any, TokenPaginatedResponse],
            self._sinch.configuration.transport.request(self.endpoint)
        )
        self._calculate_next_page()
        return self

    def auto_paging_iter(self) -> AsyncPageIterator:
        return AsyncPageIterator(self)

    @classmethod
    async def _initialize(cls, sinch: 'ClientBase', endpoint: HTTPEndpoint) -> 'AsyncTokenBasedPaginator':
        result = await cast(
            Coroutine[Any, Any, TokenPaginatedResponse],
            sinch.configuration.transport.request(endpoint)
        )
        return cls(sinch, endpoint, result)
