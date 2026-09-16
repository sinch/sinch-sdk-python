from abc import ABC, abstractmethod
from typing import Generic, Iterator, Optional
from sinch.core.endpoint import _StandardPaginatedLinkEndpoint
from sinch.core.types import BM, RM


class Paginator(ABC, Generic[RM, BM]):
    """
    Public interface for paginated list responses.

    :param RM: Result model is the server response wrapper can be accessed by :attr:`result`.
    :param BM: Body model is the type of a single item yielded by :meth:`content`/:meth:`iterator`.

    Use :meth:`content`, :meth:`next_page` and :meth:`iterator` to traverse the
    result set without dealing with the underlying pagination scheme.
    """
    def __init__(self, sinch, endpoint, result: Optional[RM] = None):
        self._sinch = sinch
        self.endpoint = endpoint
        self.result = result
        self.has_next_page = False
        self._update_has_next_page()

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
        return getattr(self.result, "content", [])

    def next_page(self) -> Optional["Paginator[RM, BM]"]:
        """
        Advance to the next page of results.

        :returns: This paginator positioned on the next page, or ``None`` if there is no further page.
        :rtype: Paginator | None
        """
        if not self.has_next_page:
            return None

        self.result = self._sinch.configuration.transport.request(self._next_page_endpoint())
        self._update_has_next_page()
        return self

    def iterator(self) -> Iterator[BM]:
        """
        Iterate over individual items across all pages, fetching each page on demand.

        :returns: An iterator over every item in the result set.
        :rtype: Iterator[BM]
        """
        paginator = self
        while paginator:
            yield from paginator.content()

            next_page_instance = paginator.next_page()
            if not next_page_instance:
                break
            paginator = next_page_instance

    def _next_page_endpoint(self):
        """Returns the endpoint the next page is requested from."""
        return self.endpoint

    @abstractmethod
    def _update_has_next_page(self):
        pass

    @classmethod
    def _initialize(cls, sinch, endpoint):
        """
        Creates an instance of the paginator, fetching the first page.
        """
        result = sinch.configuration.transport.request(endpoint)
        return cls(sinch, endpoint, result=result)


class SMSPaginator(Paginator[RM, BM]):
    """Base paginator for integer-based pagination with explicit page navigation and metadata.

    :meta private:
    """

    def _next_page_endpoint(self):
        """Calculates the page number on the paginated endpoint."""
        if self.endpoint.request_data.page is None:
            self.endpoint.request_data.page = 0
        self.endpoint.request_data.page += 1
        return self.endpoint

    def _update_has_next_page(self):
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


class LinkBasedPaginator(Paginator[RM, BM]):
    """Base paginator for link based pagination, as defined by the Sinch REST API standards.

    The next page is addressed by an absolute link served by the API through the response
    ``links`` object. The absence of a ``next`` link marks the last page.

    :meta private:
    """

    def _next_page_endpoint(self):
        """Targets the absolute link served by the API, as-is."""
        return _StandardPaginatedLinkEndpoint(self.endpoint, self._next_page_link())

    def _next_page_link(self):
        links = getattr(self.result, "links", None)
        return getattr(links, "next", None) if links else None

    def _update_has_next_page(self):
        self.has_next_page = bool(self._next_page_link())


class TokenBasedPaginator(Paginator[RM, BM]):
    """Base paginator for token-based pagination with explicit page navigation.

    :meta private:
    """

    def _next_page_endpoint(self):
        """Sets the token served by the API back into the paginated endpoint."""
        self.endpoint.request_data.page_token = self.result.next_page_token
        return self.endpoint

    def _update_has_next_page(self):
        self.has_next_page = bool(getattr(self.result, "next_page_token", None))
