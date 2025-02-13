from abc import ABC, abstractmethod
from collections import namedtuple


class PageIterator:
    def __init__(self, paginator, yield_first_page=False):
        self.paginator = paginator
        self.yield_first_page = yield_first_page
        # If yielding the first page, set started to False
        self.started = not yield_first_page

    def __iter__(self):
        return self

    def __next__(self):
        if not self.started:
            self.started = True
            return self.paginator

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
    def __init__(self, sinch, endpoint, result):
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
        return AsyncPageIterator(self)

    @classmethod
    async def _initialize(cls, sinch, endpoint):
        result = await sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result)


class TokenBasedPaginatorBase(Paginator):
    """Base paginator for token-based pagination."""

    def __init__(self, sinch, endpoint, yield_first_page=False, result=None):
        self._sinch = sinch
        self.endpoint = endpoint
        # Determines if the first page should be included
        self.yield_first_page = yield_first_page
        self.result = result or self._sinch.configuration.transport.request(self.endpoint)
        self.has_next_page = bool(self.result.next_page_token)

    def __repr__(self):
        pass

    def _calculate_next_page(self):
        self.has_next_page = bool(self.result.next_page_token)

    def next_page(self):
        """Fetches the next page and updates pagination state."""
        self.endpoint.request_data.page_token = self.result.next_page_token
        self.result = self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

    def auto_paging_iter(self):
        """Returns an iterator for automatic pagination."""
        return PageIterator(self, yield_first_page=self.yield_first_page)

    @classmethod
    def _initialize(cls, sinch, endpoint):
        """Creates an instance of the paginator skipping first page."""
        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, yield_first_page=False, result=result)


class TokenBasedPaginator(TokenBasedPaginatorBase):
    """Paginator that skips the first page."""
    pass


class TokenBasedPaginatorNumbers(TokenBasedPaginatorBase):
    """
    Paginator for handling token-based pagination specifically for phone numbers.

    This paginator is designed to iterate through phone numbers automatically or manually, fetching new pages as needed.
    It extends the TokenBasedPaginatorBase class and provides additional methods for number-specific pagination.
    """

    def __init__(self, sinch, endpoint):
        super().__init__(sinch, endpoint, yield_first_page=True)

    def numbers_iterator(self):
        """Iterates through numbers individually, fetching new pages as needed."""
        while True:
            if self.result and self.result.active_numbers:
                yield from self.result.active_numbers

            if not self.has_next_page:
                break

            self.next_page()

    def list(self):
        """Returns the first page's numbers along with pagination metadata."""

        PagedListResponse = namedtuple(
            "PagedResponse", ["result", "has_next_page", "next_page_info", "next_page"]
        )

        next_page_result = self._get_next_page_result()

        return PagedListResponse(
            result=self.result.active_numbers,
            has_next_page=self.has_next_page,
            next_page_info=self._build_next_pagination_info(next_page_result),
            next_page=self._next_page_wrapper()
        )

    def _get_next_page_result(self):
        """Fetches the next page result."""
        if not self.has_next_page:
            return None

        current_state = self.result
        self.next_page()
        next_page_result = self.result
        self.result = current_state

        return next_page_result

    def _build_next_pagination_info(self, next_page_result):
        """Constructs and returns structured pagination metadata."""
        return {
            "result": self.result.active_numbers,
            "result.next": (
                self.result.active_numbers + next_page_result.active_numbers
                if next_page_result else self.result.active_numbers
            ),
            "has_next_page": self.has_next_page,
            "has_next_page.next": bool(next_page_result and next_page_result.next_page_token),
        }

    def _next_page_wrapper(self):
        """Fetches and returns the next page as a formatted PagedListResponse object."""
        def wrapper():
            self.next_page()
            return self.list()
        return wrapper


class AsyncTokenBasedPaginator(TokenBasedPaginatorBase):
    """Asynchronous token-based paginator."""

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
        return cls(sinch, endpoint, result=result)
