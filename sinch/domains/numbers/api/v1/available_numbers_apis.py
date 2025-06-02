from typing import Optional
from pydantic import StrictInt, StrictStr

from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.domains.numbers.models.v1.response import (
    ActiveNumber, AvailableNumber
)
from sinch.domains.numbers.api.v1.base import BaseNumbers
from sinch.domains.numbers.api.v1.internal import (
    AvailableNumbersEndpoint, RentAnyNumberEndpoint, RentNumberEndpoint, SearchForNumberEndpoint
)
from sinch.domains.numbers.models.v1.internal import (
    ListAvailableNumbersRequest, NumberRequest, RentAnyNumberRequest, RentNumberRequest
)
from sinch.domains.numbers.models.v1.types import (
    CapabilityTypeValuesList, NumberPatternDict, NumberSearchPatternTypeValues,
    NumberTypeValues, SmsConfigurationDict, VoiceConfigurationDictType
)


class AvailableNumbers(BaseNumbers):

    def check_availability(self, phone_number: StrictStr, **kwargs) -> AvailableNumber:
        request_data = NumberRequest(phone_number=phone_number, **kwargs)
        return self._request(SearchForNumberEndpoint, request_data)

    def list(
        self,
        region_code: StrictStr,
        number_type: NumberTypeValues,
        number_pattern: Optional[StrictStr] = None,
        number_search_pattern: Optional[NumberSearchPatternTypeValues] = None,
        capabilities: Optional[CapabilityTypeValuesList] = None,
        page_size: Optional[StrictInt] = None,
        **kwargs
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
                    **kwargs
                )
            )
        )

    def rent(
        self,
        phone_number: StrictStr,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDictType] = None,
        callback_url: Optional[StrictStr] = None,
        **kwargs
    ) -> ActiveNumber:
        request_data = RentNumberRequest(
            phone_number=phone_number,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            callback_url=callback_url,
            **kwargs
        )
        return self._request(RentNumberEndpoint, request_data)

    def rent_any(
        self,
        region_code: StrictStr,
        type_: NumberTypeValues,
        number_pattern: Optional[NumberPatternDict] = None,
        capabilities: Optional[CapabilityTypeValuesList] = None,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDictType] = None,
        callback_url: Optional[StrictStr] = None,
        **kwargs
    ) -> ActiveNumber:
        request_data = RentAnyNumberRequest(
            region_code=region_code,
            type_=type_,
            number_pattern=number_pattern,
            capabilities=capabilities,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            callback_url=callback_url,
            **kwargs
        )
        return self._request(RentAnyNumberEndpoint, request_data)
