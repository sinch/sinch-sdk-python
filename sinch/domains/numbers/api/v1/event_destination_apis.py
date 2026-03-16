from sinch.domains.numbers.api.v1.base import BaseNumbers
from sinch.domains.numbers.api.v1.internal import (
    GetEventDestinationEndpoint,
    UpdateEventDestinationEndpoint,
)
from sinch.domains.numbers.models.v1.internal import (
    UpdateEventDestinationRequest,
)
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)
from sinch.domains.numbers.models.v1.response import (
    EventDestinationResponse,
)


class EventDestinations(BaseNumbers):
    def get(self, **kwargs) -> EventDestinationResponse:
        """
        Returns the event destination configuration for the specified project

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: The event destination configuration for the project.
        :rtype: EventDestinationResponse

        For detailed documentation, visit: https://developers.sinch.com
        """
        request_data = None
        if kwargs:
            request_data = BaseModelConfigurationRequest(**kwargs)
        return self._request(GetEventDestinationEndpoint, request_data)

    def update(self, hmac_secret: str, **kwargs) -> EventDestinationResponse:
        """
        Updates the event destination configuration for the specified project

        :param hmac_secret: The HMAC secret used to sign the event destination requests.
        :type hmac_secret: str

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: The updated event destination configuration for the project.
        :rtype: EventDestinationResponse

        For detailed documentation, visit https://developers.sinch.com
        """
        request_data = UpdateEventDestinationRequest(
            hmac_secret=hmac_secret, **kwargs
        )
        return self._request(UpdateEventDestinationEndpoint, request_data)


# Backwards-compatible alias (singular form).
# Keep until downstream users migrate to EventDestinations / event_destinations.
EventDestination = EventDestinations
