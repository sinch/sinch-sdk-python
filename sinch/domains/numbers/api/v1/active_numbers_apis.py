from typing import Optional
from pydantic import StrictStr, StrictInt
from sinch.core.pagination import TokenBasedPaginator, AsyncTokenBasedPaginator, Paginator
from sinch.domains.numbers.api.v1.base import BaseNumbers
from sinch.domains.numbers.api.v1.internal import ListActiveNumbersEndpoint
from sinch.domains.numbers.endpoints.active import (
    GetNumberConfigurationEndpoint, ReleaseNumberFromProjectEndpoint,
    UpdateNumberConfigurationEndpoint
)
from sinch.domains.numbers.models.active.requests import (
    GetNumberConfigurationRequest, UpdateNumberConfigurationRequest, ReleaseNumberFromProjectRequest
)
from sinch.domains.numbers.models.active.responses import (
    UpdateNumberConfigurationResponse, GetNumberConfigurationResponse, ReleaseNumberFromProjectResponse
)
from sinch.domains.numbers.models.v1.internal import ListActiveNumbersRequest
from sinch.domains.numbers.models.v1.response.shared import ActiveNumber
from sinch.domains.numbers.models.v1.types import (
    CapabilityTypeValuesList, NumberSearchPatternTypeValues, NumberTypeValues, OrderByValues
)


class ActiveNumbers(BaseNumbers):

    def list(
        self,
        region_code: StrictStr,
        number_type: NumberTypeValues,
        number_pattern: Optional[StrictStr] = None,
        number_search_pattern: Optional[NumberSearchPatternTypeValues] = None,
        capabilities: Optional[CapabilityTypeValuesList] = None,
        page_size: Optional[StrictInt] = None,
        page_token: Optional[StrictStr] = None,
        order_by: Optional[OrderByValues] = None,
        **kwargs
    ) -> Paginator[ActiveNumber]:
        """
        Search for all active virtual numbers associated with a certain project.

        Args:
            region_code (StrictStr): ISO 3166-1 alpha-2 country code of the phone number.
            number_type (NumberTypeValues): Type of number (e.g., "MOBILE", "LOCAL", "TOLL_FREE").
            number_pattern (Optional[StrictStr]): Specific sequence of digits to search for.
            number_search_pattern (Optional[NumberSearchPatternTypeValues]):
                Pattern to apply (e.g., "START", "CONTAINS", "END").
            capabilities (Optional[CapabilityTypeValuesList]): Capabilities required for the number.
                (e.g., ["SMS", "VOICE"])
            page_size (StrictInt): Maximum number of items to return.
            page_token (Optional[StrictStr]): Token for the next page of results.
            order_by (Optional[OrderByValues]): Field to order the results by. (e.g., "phoneNumber", "displayName")
            **kwargs: Additional filters for the request.

        Returns:
            TokenBasedPaginatorNumbers: A paginator for iterating through the results.

        For detailed documentation, visit https://developers.sinch.com
        """
        return TokenBasedPaginator(
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
                    page_token=page_token,
                    order_by=order_by,
                    **kwargs
                )
            )
        )

    # TODO: Refactor the update(), get(), release() functions to use Pydantic models:
    #       - Replace primitive types with Pydantic for better validation and maintainability.
    #       - Define Pydantic models for request and response data.
    #       - Improve readability and maintainability through refactoring.
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
        region_code: StrictStr,
        number_type: NumberTypeValues,
        number_pattern: Optional[StrictStr] = None,
        number_search_pattern: Optional[NumberSearchPatternTypeValues] = None,
        capabilities: Optional[CapabilityTypeValuesList] = None,
        page_size: Optional[StrictInt] = None,
        page_token: Optional[StrictStr] = None,
        order_by: Optional[OrderByValues] = None,
        **kwargs
    ) -> Paginator[ActiveNumber]:
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
                    page_token=page_token,
                    order_by=order_by,
                )
            )
        )
