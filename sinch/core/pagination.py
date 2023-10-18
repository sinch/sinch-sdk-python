from abc import ABC, abstractmethod
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_response import HTTPResponse
from typing import TYPE_CHECKING, Union

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
    def __init__(self, sinch: 'ClientBase', endpoint: HTTPEndpoint, result: HTTPResponse):
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
    def next_page(self) -> 'Paginator':
        pass

    @abstractmethod
    def _calculate_next_page(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def _initialize(cls, sinch: 'ClientBase', endpoint: HTTPEndpoint) -> 'Paginator':
        pass


class PageIterator:
    def __init__(self, paginator: Paginator):
        self.paginator = paginator

    def __iter__(self) -> 'PageIterator':
        return self

    def __next__(self) -> Paginator:
        if self.paginator.has_next_page:
            return self.paginator.next_page()
        else:
            raise StopIteration


class AsyncPageIterator:
    def __init__(self, paginator: Paginator):
        self.paginator = paginator

    def __aiter__(self) -> 'AsyncPageIterator':
        return self

    async def __anext__(self):
        if self.paginator.has_next_page:
            return await self.paginator.next_page()
        else:
            raise StopAsyncIteration


class IntBasedPaginator(Paginator):
    __doc__ = Paginator.__doc__

    def _calculate_next_page(self) -> None:
        if self.result.page_size:
            self.has_next_page = True
        else:
            self.has_next_page = False

    def next_page(self):
        self.endpoint.request_data.page += 1
        self.result = self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

    def auto_paging_iter(self) -> PageIterator:
        return PageIterator(self)

    @classmethod
    def _initialize(cls, sinch: 'ClientBase', endpoint: HTTPEndpoint) -> 'IntBasedPaginator':
        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)


class AsyncIntBasedPaginator(IntBasedPaginator):
    __doc__ = IntBasedPaginator.__doc__

    async def next_page(self) -> 'AsyncIntBasedPaginator':
        self.endpoint.request_data.page += 1
        self.result = await self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

    def auto_paging_iter(self) -> AsyncPageIterator:
        return AsyncPageIterator(self)

    @classmethod
    async def _initialize(cls, sinch: 'ClientBase', endpoint: HTTPEndpoint) -> 'AsyncIntBasedPaginator':
        result = await sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)


class TokenBasedPaginator(Paginator):
    __doc__ = Paginator.__doc__

    def _calculate_next_page(self) -> None:
        if self.result.next_page_token:
            self.has_next_page = True
        else:
            self.has_next_page = False

    def next_page(self) -> 'TokenBasedPaginator':
        self.endpoint.request_data.page_token = self.result.next_page_token
        self.result = self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

    def auto_paging_iter(self) -> PageIterator:
        return PageIterator(self)

    @classmethod
    def _initialize(cls, sinch: 'ClientBase', endpoint: HTTPEndpoint) -> 'TokenBasedPaginator':
        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)


class AsyncTokenBasedPaginator(TokenBasedPaginator):
    __doc__ = TokenBasedPaginator.__doc__

    async def next_page(self) -> 'AsyncTokenBasedPaginator':
        self.endpoint.request_data.page_token = self.result.next_page_token
        self.result = await self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

    def auto_paging_iter(self) -> AsyncPageIterator:
        return AsyncPageIterator(self)

    @classmethod
    async def _initialize(cls, sinch: 'ClientBase', endpoint: HTTPEndpoint) -> 'AsyncTokenBasedPaginator':
        result = await sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)
