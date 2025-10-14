from typing import Optional, List

from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.domains.numbers.models.v1.response import ActiveNumber, AvailableNumber
from sinch.domains.numbers.api.v1.base import BaseNumbers
from sinch.domains.numbers.api.v1.internal import (
    AvailableNumbersEndpoint,
    RentAnyNumberEndpoint,
    RentNumberEndpoint,
    SearchForNumberEndpoint,
)
from sinch.domains.numbers.models.v1.internal import (
    ListAvailableNumbersRequest,
    NumberRequest,
    RentAnyNumberRequest,
    RentNumberRequest,
)
from sinch.domains.numbers.models.v1.types import (
    CapabilityType,
    NumberPatternDict,
    NumberSearchPatternType,
    NumberType,
    SmsConfigurationDict,
    VoiceConfigurationDict,
)


class AvailableNumbers(BaseNumbers):

    def check_availability(self, phone_number: str, **kwargs) -> AvailableNumber:
        request_data = NumberRequest(phone_number=phone_number, **kwargs)
        return self._request(SearchForNumberEndpoint, request_data)

    def search_for_available_numbers(
        self,
        region_code: str,
        number_type: NumberType,
        number_pattern: Optional[str] = None,
        number_search_pattern: Optional[NumberSearchPatternType] = None,
        capabilities: Optional[List[CapabilityType]] = None,
        page_size: Optional[int] = None,
        **kwargs,
    ) -> Paginator[AvailableNumber]:
        return TokenBasedPaginator(
            sinch=self._sinch,
            endpoint=AvailableNumbersEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListAvailableNumbersRequest(
                    region_code=region_code,
                    number_type=number_type,
                    page_size=page_size,
                    capabilities=capabilities,
                    number_pattern=number_pattern,
                    number_search_pattern=number_search_pattern,
                    **kwargs,
                ),
            ),
        )

    def rent(
        self,
        phone_number: str,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDict] = None,
        callback_url: Optional[str] = None,
        **kwargs,
    ) -> ActiveNumber:
        request_data = RentNumberRequest(
            phone_number=phone_number,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            callback_url=callback_url,
            **kwargs,
        )
        return self._request(RentNumberEndpoint, request_data)

    def rent_any(
        self,
        region_code: str,
        number_type: NumberType,
        number_pattern: Optional[NumberPatternDict] = None,
        capabilities: Optional[List[CapabilityType]] = None,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDict] = None,
        callback_url: Optional[str] = None,
        **kwargs,
    ) -> ActiveNumber:
        request_data = RentAnyNumberRequest(
            region_code=region_code,
            number_type=number_type,
            number_pattern=number_pattern,
            capabilities=capabilities,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            callback_url=callback_url,
            **kwargs,
        )
        return self._request(RentAnyNumberEndpoint, request_data)
