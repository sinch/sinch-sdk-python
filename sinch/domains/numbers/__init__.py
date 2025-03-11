from sinch.domains.numbers.api.v1.available_numbers.available_numbers_apis import AvailableNumbers
from sinch.domains.numbers.api.v1.active_numbers.active_numbers_apis import (
    ActiveNumbers, ActiveNumbersWithAsyncPagination
)
from sinch.domains.numbers.endpoints.callbacks.get_configuration import GetNumbersCallbackConfigurationEndpoint
from sinch.domains.numbers.endpoints.callbacks.update_configuration import UpdateNumbersCallbackConfigurationEndpoint
from sinch.domains.numbers.endpoints.regions.list_available_regions import ListAvailableRegionsEndpoint

from sinch.domains.numbers.models.regions.requests import ListAvailableRegionsForProjectRequest
from sinch.domains.numbers.models.regions.responses import ListAvailableRegionsResponse
from sinch.domains.numbers.models.callbacks.responses import (
    GetNumbersCallbackConfigurationResponse,
    UpdateNumbersCallbackConfigurationResponse
)
from sinch.domains.numbers.models.callbacks.requests import (
    UpdateNumbersCallbackConfigurationRequest
)


class AvailableRegions:
    def __init__(self, sinch):
        self._sinch = sinch

    def list(
        self,
        number_type: str = None,
        number_types: list = None
    ) -> ListAvailableRegionsResponse:
        """
        Lists all regions for numbers provided using the project ID.
        Some numbers can be configured for multiple regions.
        See which regions apply to your virtual number.
        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        return self._sinch.configuration.transport.request(
            ListAvailableRegionsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListAvailableRegionsForProjectRequest(
                    number_type=number_type,
                    number_types=number_types
                )
            )
        )


class Callbacks:
    def __init__(self, sinch):
        self._sinch = sinch

    def get_configuration(self) -> GetNumbersCallbackConfigurationResponse:
        return self._sinch.configuration.transport.request(
            GetNumbersCallbackConfigurationEndpoint(
                project_id=self._sinch.configuration.project_id
            )
        )

    def update_configuration(self, hmac_secret) -> UpdateNumbersCallbackConfigurationResponse:
        return self._sinch.configuration.transport.request(
            UpdateNumbersCallbackConfigurationEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=UpdateNumbersCallbackConfigurationRequest(
                    hmac_secret=hmac_secret
                )
            )
        )


class NumbersBase:
    """
    Documentation for Sinch virtual Numbers is found at https://developers.sinch.com/docs/numbers/.
    """
    def __init__(self, sinch):
        self._sinch = sinch


class Numbers(NumbersBase):
    """
    Synchronous version of the Numbers Domain
    """
    __doc__ += NumbersBase.__doc__

    def __init__(self, sinch):
        super(Numbers, self).__init__(sinch)
        self.available = AvailableNumbers(self._sinch)
        self.regions = AvailableRegions(self._sinch)
        self.active = ActiveNumbers(self._sinch)
        self.callbacks = Callbacks(self._sinch)


class NumbersAsync(NumbersBase):
    """
    Asynchronous version of the Numbers Domain
    """
    __doc__ += NumbersBase.__doc__

    def __init__(self, sinch):
        super(NumbersAsync, self).__init__(sinch)
        self.available = AvailableNumbers(self._sinch)
        self.regions = AvailableRegions(self._sinch)
        self.active = ActiveNumbersWithAsyncPagination(self._sinch)
        self.callbacks = Callbacks(self._sinch)
