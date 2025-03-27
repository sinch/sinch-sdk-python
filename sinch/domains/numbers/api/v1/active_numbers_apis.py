from typing import Optional, overload
from pydantic import StrictStr, StrictInt
from sinch.core.pagination import TokenBasedPaginator, AsyncTokenBasedPaginator, Paginator
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
    CapabilityTypeValuesList, NumberSearchPatternTypeValues, NumberTypeValues, OrderByValues,
    SmsConfigurationDict, VoiceConfigurationDictType, VoiceConfigurationDictFAX, VoiceConfigurationDictRTC,
    VoiceConfigurationDictEST
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

        :param region_code: ISO 3166-1 alpha-2 country code of the phone number.
        :type region_code: StrictStr

        :param number_type: Type of number (e.g., "MOBILE", "LOCAL", "TOLL_FREE").
        :type number_type: NumberTypeValues

        :param number_pattern: Specific sequence of digits to search for.
        :type number_pattern: Optional[StrictStr]

        :param number_search_pattern: Pattern to apply (e.g., "START", "CONTAINS", "END").
        :type number_search_pattern: Optional[NumberSearchPatternTypeValues]

        :param capabilities: Capabilities required for the number (e.g., ["SMS", "VOICE"]).
        :type capabilities: Optional[CapabilityTypeValuesList]

        :param page_size: Maximum number of items to return.
        :type page_size: StrictInt

        :param page_token: Token for the next page of results.
        :type page_token: Optional[StrictStr]

        :param order_by: Field to order the results by (e.g., "phoneNumber", "displayName").
        :type order_by: Optional[OrderByValues]

        :param kwargs: Additional filters for the request.
        :type kwargs: dict

        :returns: A paginator for iterating through the results.
        :rtype: Paginator[ActiveNumber]

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

    @overload
    def update(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictEST,
            display_name: Optional[StrictStr] = None,
            callback_url: Optional[StrictStr] = None
    ) -> ActiveNumber:
        pass

    @overload
    def update(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictFAX,
            display_name: Optional[StrictStr] = None,
            callback_url: Optional[StrictStr] = None
    ) -> ActiveNumber:
        pass

    @overload
    def update(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictRTC,
            display_name: Optional[StrictStr] = None,
            callback_url: Optional[StrictStr] = None
    ) -> ActiveNumber:
        pass

    def update(
        self,
        phone_number: StrictStr,
        display_name: Optional[StrictStr] = None,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDictType] = None,
        callback_url: Optional[StrictStr] = None,
        **kwargs
    ) -> ActiveNumber:
        """
        Make updates to the configuration of your virtual number.
        Update the display name, change the currency type, or reconfigure for either SMS and/or Voice.

        :param phone_number: The phone number in E.164 format with leading +.
        :type phone_number: str

        :param display_name: The display name for the virtual number.
        :type display_name: Optional[str]

        :param sms_configuration: A dictionary defining the SMS configuration. Including fields such as:
                                  - ``service_plan_id`` (str): The service plan ID.
                                  - ``campaign_id`` (Optional[str]): The campaign ID.
        :type sms_configuration: Optional[SmsConfigurationDict]

        :param voice_configuration: A dictionary defining the Voice configuration. Supported types include:
                                    - ``VoiceConfigurationDictRTC``: type 'RTC' with an ``app_id`` field.
                                    - ``VoiceConfigurationDictEST``: type 'EST' with a ``trunk_id`` field.
                                    - ``VoiceConfigurationDictFAX``: type 'FAX' with a ``service_id`` field.
        :type voice_configuration: Optional[VoiceConfigurationDictType]

        :param callback_url: The callback URL for the virtual number.
        :type callback_url: Optional[str]

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        For detailed documentation, visit https://developers.sinch.com
        """
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
        """
        List of configuration settings for your virtual number.

        :param phone_number: The phone number in E.164 format with leading +.
        :type phone_number: str

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: The configuration settings for the virtual number.
        :rtype: ActiveNumber

        For detailed documentation, visit https://developers.sinch.com
        """
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
        """
        Release virtual numbers you no longer need from your project.

        :param phone_number: The phone number in E.164 format with leading +.
        :type phone_number: str

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: The configuration settings of the released virtual number.
        :rtype: ActiveNumber

        For detailed documentation, visit https://developers.sinch.com
        """
        request_data = NumberRequest(
            phone_number=phone_number,
            **kwargs
        )
        return self._request(ReleaseNumberFromProjectEndpoint, request_data)


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
