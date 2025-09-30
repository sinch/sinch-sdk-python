from typing import Optional, List
from sinch.core.pagination import TokenBasedPaginator, Paginator
from sinch.domains.numbers.api.v1.internal import ListAvailableRegionsEndpoint
from sinch.domains.numbers.models.v1.internal import ListAvailableRegionsRequest
from sinch.domains.numbers.models.v1.response import AvailableRegion
from sinch.domains.numbers.models.v1.types import NumberType


class AvailableRegions:
    def __init__(self, sinch):
        self._sinch = sinch

    def list(
        self,
        types: Optional[List[NumberType]] = None,
        **kwargs
    ) -> Paginator[AvailableRegion]:
        """
        Lists all regions for numbers provided using the project ID.
        Some numbers can be configured for multiple regions.
        See which regions apply to your virtual number.

        :param types: List of number types to filter the regions.
        :type types: Optional[List[NumberType]]

        :param kwargs: Additional parameters for the request.
        :type kwargs: Optional[dict]

        :return: A paginator object containing the list of available regions.
        :rtype: Paginator[Region]

        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        return TokenBasedPaginator(
            sinch=self._sinch,
            endpoint=ListAvailableRegionsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListAvailableRegionsRequest(
                    types=types,
                    **kwargs
                )
            )
        )
