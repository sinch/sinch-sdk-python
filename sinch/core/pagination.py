from abc import ABC, abstractmethod
from typing import Generic, Iterator
from sinch.core.types import BM


class Paginator(ABC, Generic[BM]):
    """
    Public interface for paginated list responses.

    Use :meth:`content`, :meth:`next_page` and :meth:`iterator` to traverse the
    result set without dealing with the underlying pagination scheme.
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
    def content(self) -> list[BM]:
        """
        Return the items contained in the current page.

        :returns: The list of items in the current page.
        :rtype: list[BM]
        """
        pass

    # TODO: Make iterator() method abstract in Parent class as we implement in the other domains:
    #  - Refactor pydantic models in other domains to have a content property.
    def iterator(self) -> Iterator[BM]:
        """
        Iterate over individual items across all pages, fetching each page on demand.

        :returns: An iterator over every item in the result set.
        :rtype: Iterator[BM]
        """
        pass

    @abstractmethod
    def next_page(self):
        """
        Advance to the next page of results.

        :returns: This paginator positioned on the next page, or ``None`` if there is no further page.
        :rtype: Paginator | None
        """
        pass

    @abstractmethod
    def _calculate_next_page(self):
        pass

    @classmethod
    @abstractmethod
    def _initialize(cls, sinch, endpoint):
        pass


class SMSPaginator(Paginator[BM]):
    """Base paginator for integer-based pagination with explicit page navigation and metadata.

    :meta private:
    """

    def __init__(self, sinch, endpoint, result=None):
        super().__init__(sinch, endpoint, result or sinch.configuration.transport.request(endpoint))

    def content(self) -> list[BM]:
        """Returns the content list from the result."""
        return getattr(self.result, "content", [])

    def next_page(self):
        """Returns a new paginator instance for the next page."""
        if not self.has_next_page:
            return None

        if self.endpoint.request_data.page is None:
            self.endpoint.request_data.page = 0
        self.endpoint.request_data.page += 1
        self.result = self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

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
        """Calculates if there's a next page based on count, page, and effective page_size."""
        count = getattr(self.result, 'count', None)
        page = getattr(self.result, 'page', None)
        page_size = getattr(self.result, 'page_size', None)

        if count is None or page is None or page_size is None:
            self.has_next_page = False
            return
        
        if not self.content():
            self.has_next_page = False
            return

        # Cache first response page_size when not provided in order to calculate next pages correctly
        request_page_size = self.endpoint.request_data.page_size
        if request_page_size is None:
            if not hasattr(self, '_first_response_page_size'):
                self._first_response_page_size = page_size
            request_page_size = self._first_response_page_size

        total_pages = (count + request_page_size - 1) // request_page_size
        self.has_next_page = page < (total_pages - 1)
        

    @classmethod
    def _initialize(cls, sinch, endpoint):
        """Creates an instance of the paginator skipping first page."""
        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result=result)


class TokenBasedPaginator(Paginator[BM]):
    """Base paginator for token-based pagination with explicit page navigation and metadata.

    :meta private:
    """

    def __init__(self, sinch, endpoint, result=None):
        super().__init__(sinch, endpoint, result or sinch.configuration.transport.request(endpoint))

    def content(self) -> list[BM]:
        return getattr(self.result, "content", [])

    def next_page(self):
        """Returns a new paginator instance for the next page."""
        if not self.has_next_page:
            return None

        self.endpoint.request_data.page_token = self.result.next_page_token
        self.result = self._sinch.configuration.transport.request(self.endpoint)
        self._calculate_next_page()
        return self

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
        return cls(sinch, endpoint, result=result)
