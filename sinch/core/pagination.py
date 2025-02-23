from abc import ABC, abstractmethod
from typing import Generic
from sinch.core.types import BM


class PageIterator:
    def __init__(self, paginator, yield_first_page=False):
        self.paginator = paginator
        # If yielding the first page, set started to False
        self.started = not yield_first_page

    def __iter__(self):
        return self

    def __next__(self):
        if not self.started:
            self.started = True
            return self.paginator

        if self.paginator.has_next_page:
            self.paginator = self.paginator.next_page()
            return self.paginator
        else:
            raise StopIteration


class AsyncPageIterator:
    def __init__(self, paginator, yield_first_page=False):
        self.paginator = paginator
        self.started = not yield_first_page

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.started:
            self.started = True
            return self.paginator

        if self.paginator.has_next_page:
            next_paginator = await self.paginator.next_page()
            if next_paginator:
                self.paginator = next_paginator
                return self.paginator
        else:
            raise StopAsyncIteration


class Paginator(ABC, Generic[BM]):
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
    def __init__(self, sinch, endpoint, result: BM):
        self._sinch = sinch
        self.result = result
        self.endpoint = endpoint
        self.has_next_page = False
        self._calculate_next_page()

    def __repr__(self):
        return "Paginated response content: " + str(self.result)

    # TODO: Make content() method abstract in Parent class as we implement in the other domains:
    #  - Refactor pydantic models in other domains to have a content property.
    def content(self):
        pass

    # TODO: Make iterator() method abstract in Parent class as we implement in the other domains:
    #  - Refactor pydantic models in other domains to have a content property.
    def iterator(self):
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


class IntBasedPaginator(Paginator):
    __doc__ = Paginator.__doc__

    def _calculate_next_page(self):
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
    def _initialize(cls, sinch, endpoint):
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
        return AsyncPageIterator(self, yield_first_page=True)

    @classmethod
    async def _initialize(cls, sinch, endpoint):
        result = await sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)


class TokenBasedPaginator(Paginator[BM]):
    """Base paginator for token-based pagination with explicit page navigation and metadata."""

    def __init__(self, sinch, endpoint, yield_first_page=False, result=None):
        super().__init__(sinch, endpoint, result or sinch.configuration.transport.request(endpoint))

    def content(self) -> list[BM]:
        return getattr(self.result, "content", [])

    def next_page(self):
        """Returns a new paginator instance for the next page."""
        if not self.has_next_page:
            return None

        self.endpoint.request_data.page_token = self.result.next_page_token
        next_result = self._sinch.configuration.transport.request(self.endpoint)

        return self.__class__(self._sinch, self.endpoint, result=next_result)

    def iterator(self):
        """Iterates over individual items across all pages."""
        paginator = self
        while paginator:
            yield from paginator.content()

            next_page_instance = paginator.next_page()
            if not next_page_instance:
                break
            paginator = next_page_instance

    def _calculate_next_page(self):
        self.has_next_page = bool(getattr(self.result, "next_page_token", None))

    @classmethod
    def _initialize(cls, sinch, endpoint):
        """Creates an instance of the paginator skipping first page."""
        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, yield_first_page=False, result=result)


class AsyncTokenBasedPaginator(TokenBasedPaginator):
    """Asynchronous token-based paginator."""

    async def next_page(self):
        if not self.has_next_page:
            return None

        self.endpoint.request_data.page_token = self.result.next_page_token
        next_result = await self._sinch.configuration.transport.request(self.endpoint)

        return self.__class__(self._sinch, self.endpoint, result=next_result)

    async def iterator(self):
        """Iterates asynchronously over individual items across all pages."""
        paginator = self
        while paginator:
            for item in paginator.content():
                yield item

            next_page_instance = await paginator.next_page()
            if not next_page_instance:
                break
            paginator = next_page_instance

    @classmethod
    async def _initialize(cls, sinch, endpoint):
        result = await sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, yield_first_page=False, result=result)
