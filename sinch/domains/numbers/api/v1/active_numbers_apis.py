from typing import Optional
from pydantic import StrictStr, StrictInt, conlist
from sinch.core.pagination import TokenBasedPaginator, Paginator
from sinch.domains.numbers.api.v1.base import BaseNumbers
from sinch.domains.numbers.api.v1.internal import (
    GetNumberConfigurationEndpoint, ListActiveNumbersEndpoint, ReleaseNumberFromProjectEndpoint,
    UpdateNumberConfigurationEndpoint
)
from sinch.domains.numbers.models.v1.response import ActiveNumber

from sinch.domains.numbers.models.v1.internal import (
    ListActiveNumbersRequest, NumberRequest, UpdateNumberConfigurationRequest
)
from sinch.domains.numbers.models.v1.types import (
    CapabilityTypeValues, NumberSearchPatternTypeValues, NumberTypeValues, OrderByValues,
    SmsConfigurationDict, VoiceConfigurationDictType
)


class ActiveNumbers(BaseNumbers):

    def list(
        self,
        region_code: StrictStr,
        number_type: NumberTypeValues,
        number_pattern: Optional[StrictStr] = None,
        number_search_pattern: Optional[NumberSearchPatternTypeValues] = None,
        capabilities: Optional[conlist(CapabilityTypeValues)] = None,
        page_size: Optional[StrictInt] = None,
        page_token: Optional[StrictStr] = None,
        order_by: Optional[OrderByValues] = None,
        **kwargs
    ) -> Paginator[ActiveNumber]:
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

    def update(
        self,
        phone_number: StrictStr,
        display_name: Optional[StrictStr] = None,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDictType] = None,
        callback_url: Optional[StrictStr] = None,
        **kwargs
    ) -> ActiveNumber:
        request_data = UpdateNumberConfigurationRequest(
            phone_number=phone_number,
            display_name=display_name,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            callback_url=callback_url,
            **kwargs
        )
        return self._request(UpdateNumberConfigurationEndpoint, request_data)

    def get(
        self,
        phone_number: StrictStr,
        **kwargs
    ) -> ActiveNumber:
        request_data = NumberRequest(
            phone_number=phone_number,
            **kwargs
        )
        return self._request(GetNumberConfigurationEndpoint, request_data)

    def release(
            self,
            phone_number: StrictStr,
            **kwargs
    ) -> ActiveNumber:
        request_data = NumberRequest(
            phone_number=phone_number,
            **kwargs
        )
        return self._request(ReleaseNumberFromProjectEndpoint, request_data)
