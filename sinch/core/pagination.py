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


class Paginator(ABC, Generic[BM]):
    """
    Pagination response object.
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


class SMSPaginator(Paginator[BM]):
    """Base paginator for integer-based pagination with explicit page navigation and metadata."""

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
        """Calculates if there's a next page based on count, page, and page_size."""
        if hasattr(self.result, 'count') and hasattr(self.result, 'page'):
            # Use the requested page_size from the endpoint
            request_page_size = self.endpoint.request_data.page_size or 1
            if request_page_size > 0 and hasattr(self.result, 'page_size'):
                # Calculate total pages needed using the request page_size
                total_pages = (self.result.count + request_page_size - 1) // request_page_size
                # Check if current page is less than total pages - 1 (0-indexed)
                self.has_next_page = self.result.page < (total_pages - 1)
            else:
                self.has_next_page = False
        else:
            self.has_next_page = False

    @classmethod
    def _initialize(cls, sinch, endpoint):
        """Creates an instance of the paginator skipping first page."""
        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result=result)


class TokenBasedPaginator(Paginator[BM]):
    """Base paginator for token-based pagination with explicit page navigation and metadata."""

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
