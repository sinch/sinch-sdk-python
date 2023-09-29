from abc import ABC, abstractmethod
from sinch.core.clients.sinch_client_base import ClientBase
from sinch.core.endpoint import HTTPEndpoint


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
    def __init__(self, sinch: ClientBase, endpoint: HTTPEndpoint, result):
        self._sinch = sinch
        self.result = result
        self.endpoint = endpoint
        self.has_next_page = False
        self._calculate_next_page()

    def __repr__(self):
        return "Paginated response content: " + str(self.result)

    @abstractmethod
    def auto_paging_iter(self):
        pass

    @abstractmethod
    def next_page(self):
        pass

    @abstractmethod
    def _calculate_next_page(self):
        pass

    @classmethod
    @abstractmethod
    def _initialize(cls, sinch, endpoint):
        pass


class PageIterator:
    def __init__(self, paginator: Paginator):
        self.paginator = paginator

    def __iter__(self):
        return self

    def __next__(self):
        if self.paginator.has_next_page:
            return self.paginator.next_page()
        else:
            raise StopIteration


class AsyncPageIterator:
    def __init__(self, paginator):
        self.paginator = paginator

    def __aiter__(self):
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

    def auto_paging_iter(self):
        return PageIterator(self)

    @classmethod
    def _initialize(cls, sinch: ClientBase, endpoint: HTTPEndpoint):
        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)


class AsyncIntBasedPaginator(IntBasedPaginator):
    __doc__ = IntBasedPaginator.__doc__

    async def next_page(self):
        self.endpoint.request_data.page += 1
        self.result = await self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

    def auto_paging_iter(self):
        return AsyncPageIterator(self)

    @classmethod
    async def _initialize(cls, sinch: ClientBase, endpoint: HTTPEndpoint):
        result = await sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)


class TokenBasedPaginator(Paginator):
    __doc__ = Paginator.__doc__

    def _calculate_next_page(self):
        if self.result.next_page_token:
            self.has_next_page = True
        else:
            self.has_next_page = False

    def next_page(self):
        self.endpoint.request_data.page_token = self.result.next_page_token
        self.result = self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

    def auto_paging_iter(self):
        return PageIterator(self)

    @classmethod
    def _initialize(cls, sinch, endpoint):
        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)


class AsyncTokenBasedPaginator(TokenBasedPaginator):
    __doc__ = TokenBasedPaginator.__doc__

    async def next_page(self):
        self.endpoint.request_data.page_token = self.result.next_page_token
        self.result = await self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

    def auto_paging_iter(self):
        return AsyncPageIterator(self)

    @classmethod
    async def _initialize(cls, sinch, endpoint):
        result = await sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)
