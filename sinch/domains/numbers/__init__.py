from sinch.core.pagination import TokenBasedPaginator, AsyncTokenBasedPaginator
from sinch.domains.numbers.endpoints.search_for_number import SearchForNumberEndpoint
from sinch.domains.numbers.endpoints.list_available_numbers import AvailableNumbersEndpoint
from sinch.domains.numbers.endpoints.activate_number import ActivateNumberEndpoint
from sinch.domains.numbers.endpoints.list_active_numbers_for_project import ListActiveNumbersEndpoint
from sinch.domains.numbers.endpoints.update_number_configuration import UpdateNumberConfigurationEndpoint
from sinch.domains.numbers.endpoints.get_number_configuration import GetNumberConfigurationEndpoint
from sinch.domains.numbers.endpoints.release_number_from_project import ReleaseNumberFromProjectEndpoint
from sinch.domains.numbers.endpoints.list_available_regions import ListAvailableRegionsEndpoint

from sinch.domains.numbers.models.requests import (
    ListAvailableNumbersRequest,
    ActivateNumberRequest,
    CheckNumberAvailabilityRequest,
    ListActiveNumbersRequest,
    GetNumberConfigurationRequest,
    ReleaseNumberFromProjectRequest,
    ListAvailableRegionsForProjectRequest,
    UpdateNumberConfigurationRequest
)

from sinch.domains.numbers.models.responses import (
    ListAvailableNumbersResponse,
    ActivateNumberResponse,
    CheckNumberAvailabilityResponse,
    ListActiveNumbersResponse,
    UpdateNumberConfigurationResponse,
    GetNumberConfigurationResponse,
    ReleaseNumberFromProjectResponse,
    ListAvailableRegionsResponse
)


class AvailableNumbers:
    def __init__(self, sinch):
        self._sinch = sinch

    def list(
        self,
        region_code: str,
        number_type: str,
        number_pattern: str = None,
        number_search_pattern: str = None,
        capabilities: list = None,
        page_size: int = None
    ) -> ListAvailableNumbersResponse:
        """
        Search for available virtual numbers using a variety of parameters to filter results.
        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        return self._sinch.configuration.transport.request(
            AvailableNumbersEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListAvailableNumbersRequest(
                    region_code=region_code,
                    number_type=number_type,
                    page_size=page_size,
                    capabilities=capabilities,
                    number_search_pattern=number_search_pattern,
                    number_pattern=number_pattern
                )
            )
        )

    def activate(
        self,
        phone_number: str,
        sms_configuration: dict = None,
        voice_configuration: dict = None
    ) -> ActivateNumberResponse:
        """
        Activate a virtual number to use with SMS products, Voice products, or both.
        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        return self._sinch.configuration.transport.request(
            ActivateNumberEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ActivateNumberRequest(
                    phone_number=phone_number,
                    sms_configuration=sms_configuration,
                    voice_configuration=voice_configuration
                )
            )
        )

    def check_availability(self, phone_number: str) -> CheckNumberAvailabilityResponse:
        """
        Enter a specific phone number to check availability.
        For additional documentation, see https://www.sinch.com and visit our developer portal.
        """
        return self._sinch.configuration.transport.request(
            SearchForNumberEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=CheckNumberAvailabilityRequest(
                    phone_number=phone_number
                )
            )
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
