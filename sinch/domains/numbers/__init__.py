from sinch.core.pagination import TokenBasedPaginator, AsyncTokenBasedPaginator
from sinch.domains.numbers.available_numbers import AvailableNumbers
from sinch.domains.numbers.endpoints.callbacks.get_configuration import GetNumbersCallbackConfigurationEndpoint
from sinch.domains.numbers.endpoints.callbacks.update_configuration import UpdateNumbersCallbackConfigurationEndpoint
from sinch.domains.numbers.endpoints.active.list_active_numbers_for_project import ListActiveNumbersEndpoint
from sinch.domains.numbers.endpoints.active.update_number_configuration import UpdateNumberConfigurationEndpoint
from sinch.domains.numbers.endpoints.active.get_number_configuration import GetNumberConfigurationEndpoint
from sinch.domains.numbers.endpoints.active.release_number_from_project import ReleaseNumberFromProjectEndpoint
from sinch.domains.numbers.endpoints.regions.list_available_regions import ListAvailableRegionsEndpoint

from sinch.domains.numbers.models.regions.requests import ListAvailableRegionsForProjectRequest
from sinch.domains.numbers.models.active.requests import (
    ListActiveNumbersRequest, GetNumberConfigurationRequest,
    UpdateNumberConfigurationRequest, ReleaseNumberFromProjectRequest
)
from sinch.domains.numbers.models.regions.responses import ListAvailableRegionsResponse
from sinch.domains.numbers.models.active.responses import (
    ListActiveNumbersResponse, UpdateNumberConfigurationResponse,
    GetNumberConfigurationResponse, ReleaseNumberFromProjectResponse
)
from sinch.domains.numbers.models.callbacks.responses import (
    GetNumbersCallbackConfigurationResponse,
    UpdateNumbersCallbackConfigurationResponse
)
from sinch.domains.numbers.models.callbacks.requests import (
    UpdateNumbersCallbackConfigurationRequest
)


class ActiveNumbers:
    def __init__(self, sinch):
        self._sinch = sinch

    def list(
        self,
        region_code: str,
        number_type: str,
        number_pattern: str = None,
        number_search_pattern: str = None,
        capabilities: list = None,
        page_size: int = None,
        page_token: str = None
    ) -> ListActiveNumbersResponse:
        """
        Search for all active virtual numbers associated with a certain project.
        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListActiveNumbersEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListActiveNumbersRequest(
                    region_code=region_code,
                    number_type=number_type,
                    page_size=page_size,
                    capabilities=capabilities,
                    number_pattern=number_pattern,
                    number_search_pattern=number_search_pattern,
                    page_token=page_token
                )
            )
        )

    def update(
        self,
        phone_number: str = None,
        display_name: str = None,
        sms_configuration: dict = None,
        voice_configuration: dict = None,
        app_id: str = None
    ) -> UpdateNumberConfigurationResponse:
        """
        Make updates to the configuration of your virtual number.
        Update the display name, change the currency type, or reconfigure for either SMS and/or Voice.
        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        return self._sinch.configuration.transport.request(
            UpdateNumberConfigurationEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=UpdateNumberConfigurationRequest(
                    phone_number=phone_number,
                    display_name=display_name,
                    sms_configuration=sms_configuration,
                    voice_configuration=voice_configuration,
                    app_id=app_id
                )
            )
        )

    def get(self, phone_number: str) -> GetNumberConfigurationResponse:
        """
        List of configuration settings for your virtual number.
        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        return self._sinch.configuration.transport.request(
            GetNumberConfigurationEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=GetNumberConfigurationRequest(
                    phone_number=phone_number
                )
            )
        )

    def release(self, phone_number: str) -> ReleaseNumberFromProjectResponse:
        """
        Release numbers you no longer need from your project.
        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        return self._sinch.configuration.transport.request(
            ReleaseNumberFromProjectEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ReleaseNumberFromProjectRequest(
                    phone_number=phone_number
                )
            )
        )


class ActiveNumbersWithAsyncPagination(ActiveNumbers):
    async def list(
        self,
        region_code: str,
        number_type: str,
        number_pattern: str = None,
        number_search_pattern: str = None,
        capabilities: list = None,
        page_size: int = None,
        page_token: str = None
    ) -> ListActiveNumbersResponse:
        return await AsyncTokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListActiveNumbersEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListActiveNumbersRequest(
                    region_code=region_code,
                    number_type=number_type,
                    page_size=page_size,
                    capabilities=capabilities,
                    number_pattern=number_pattern,
                    number_search_pattern=number_search_pattern,
                    page_token=page_token
                )
            )
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
