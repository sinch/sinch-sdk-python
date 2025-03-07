from typing import Optional, overload
from pydantic import StrictInt, StrictStr
from sinch.domains.numbers.base_numbers import (
    BaseNumbers, SmsConfigurationDict, VoiceConfigurationDictRTC, VoiceConfigurationDictType,
    VoiceConfigurationDictEST, VoiceConfigurationDictFAX, NumberPatternDict)
from sinch.domains.numbers.endpoints.available import (
    ActivateNumberEndpoint, AvailableNumbersEndpoint, RentAnyNumberEndpoint, SearchForNumberEndpoint
)
from sinch.domains.numbers.models.available import (
    ActivateNumberRequest, CheckNumberAvailabilityRequest, ListAvailableNumbersRequest, RentAnyNumberRequest
)
from sinch.domains.numbers.models.available import (
    CheckNumberAvailabilityResponse, RentAnyNumberResponse
)
from sinch.domains.numbers.models.numbers import (
    ActiveNumber, CapabilityTypeValuesList, Number, NumberSearchPatternTypeValues, NumberTypeValues
)


class AvailableNumbers(BaseNumbers):

    def list(
        self,
        region_code: StrictStr,
        number_type: NumberTypeValues,
        number_pattern: Optional[StrictStr] = None,
        number_search_pattern: Optional[NumberSearchPatternTypeValues] = None,
        capabilities: Optional[CapabilityTypeValuesList] = None,
        page_size: Optional[StrictInt] = None,
        **kwargs
    ) -> list[Number]:
        """
        Search for available virtual numbers for you to activate using a variety of parameters to filter results.

        Args:
            region_code (StrictStr): ISO 3166-1 alpha-2 country code of the phone number.
            number_type (NumberType): Type of number (e.g., "MOBILE", "LOCAL", "TOLL_FREE").
            number_pattern (Optional[StrictStr]): Specific sequence of digits to search for.
            number_search_pattern (Optional[NumberSearchPatternType]):
                Pattern to apply (e.g., "START", "CONTAINS", "END").
            capabilities (Optional[CapabilityType]): Capabilities required for the number. (e.g., ["SMS", "VOICE"])
            page_size (StrictInt): Maximum number of items to return.
            **kwargs: Additional filters for the request.

        Returns:
            list[Number]: A response array with available numbers and their details.

        For detailed documentation, visit https://developers.sinch.com
        """
        request_data = ListAvailableNumbersRequest(
            region_code=region_code,
            number_type=number_type,
            page_size=page_size,
            capabilities=capabilities,
            number_search_pattern=number_search_pattern,
            number_pattern=number_pattern,
            **kwargs
        )

        return self._request(AvailableNumbersEndpoint, request_data)

    @overload
    def activate(
            self,
            phone_number: StrictStr,
            sms_configuration: Optional[SmsConfigurationDict] = None,
            voice_configuration: Optional[VoiceConfigurationDictType] = None,
            callback_url: Optional[StrictStr] = None
    ) -> ActiveNumber:
        pass

    @overload
    def activate(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictEST,
            callback_url: Optional[StrictStr] = None
    ) -> ActiveNumber:
        pass

    @overload
    def activate(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictFAX,
            callback_url: Optional[StrictStr] = None
    ) -> ActiveNumber:
        pass

    @overload
    def activate(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictRTC,
            callback_url: Optional[StrictStr] = None
    ) -> ActiveNumber:
        pass

    def activate(
        self,
        phone_number: StrictStr,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDictType] = None,
        callback_url: Optional[StrictStr] = None,
        **kwargs
    ) -> ActiveNumber:
        """
        Activate a virtual number to use with SMS, Voice, or both products.

        Args:
            phone_number (StrictStr): The phone number in E.164 format with leading +.
            sms_configuration (Optional[SmsConfigurationDict]): A dictionary defining the SMS configuration.
                Including fields such as:
                    - service_plan_id (str): The service plan ID.
                    - campaign_id (Optional[str]): The campaign ID.
            voice_configuration (Optional[VoiceConfigurationDictType]): A dictionary defining the Voice configuration.
                Supported types include:
                    - `VoiceConfigurationDictRTC`: type 'RTC' with an `app_id` field.
                    - `VoiceConfigurationDictEST`: type 'EST' with a `trunk_id` field.
                    - `VoiceConfigurationDictFAX`: type 'FAX' with a `service_id` field.
            callback_url (Optional[StrictStr]): The callback URL to be called.
            **kwargs: Additional parameters for the request.

        Returns:
            ActiveNumber: A response object with the activated number and its details.

        For detailed documentation, visit https://developers.sinch.com
        """
        request_data = ActivateNumberRequest(
            phone_number=phone_number,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            callback_url=callback_url,
            **kwargs
        )
        return self._request(ActivateNumberEndpoint, request_data)

    @overload
    def rent_any(
            self,
            region_code: StrictStr,
            type_: NumberTypeValues,
            sms_configuration: None,
            voice_configuration: None,
            number_pattern: Optional[NumberPatternDict] = None,
            capabilities: Optional[CapabilityTypeValuesList] = None,
            callback_url: Optional[StrictStr] = None,
    ) -> RentAnyNumberResponse:
        pass

    @overload
    def rent_any(
            self,
            region_code: StrictStr,
            type_: NumberTypeValues,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictRTC,
            number_pattern: Optional[NumberPatternDict] = None,
            capabilities: Optional[CapabilityTypeValuesList] = None,
            callback_url: Optional[StrictStr] = None,
    ) -> RentAnyNumberResponse:
        pass

    @overload
    def rent_any(
            self,
            region_code: StrictStr,
            type_: NumberTypeValues,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictFAX,
            number_pattern: Optional[NumberPatternDict] = None,
            capabilities: Optional[CapabilityTypeValuesList] = None,
            callback_url: Optional[StrictStr] = None,
    ) -> RentAnyNumberResponse:
        pass

    @overload
    def rent_any(
            self,
            region_code: StrictStr,
            type_: NumberTypeValues,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictEST,
            number_pattern: Optional[NumberPatternDict] = None,
            capabilities: Optional[CapabilityTypeValuesList] = None,
            callback_url: Optional[StrictStr] = None,
    ) -> RentAnyNumberResponse:
        pass

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
    ) -> RentAnyNumberResponse:
        """
        Search for and activate an available Sinch virtual number all in one API call.
        Currently, the rentAny operation works only for US 10DLC numbers

        Args:
            region_code (str): ISO 3166-1 alpha-2 country code of the phone number.
            type_ (NumberType): Type of number (e.g., "MOBILE", "LOCAL", "TOLL_FREE").
            number_pattern (Optional[NumberPatternDict]): Specific sequence of digits to search for.
            capabilities (Optional[CapabilityType]): Capabilities required for the number. (e.g., ["SMS", "VOICE"])
            sms_configuration (Optional[SmsConfigurationDict]): A dictionary defining the SMS configuration.
                Including fields such as:
                    - service_plan_id (str): The service plan ID.
                    - campaign_id (Optional[str]): The campaign ID.
            voice_configuration (Optional[VoiceConfigurationDictType]): A dictionary defining the Voice configuration.
                Supported types include:
                    - `VoiceConfigurationDictRTC`: type 'RTC' with an `app_id` field.
                    - `VoiceConfigurationDictEST`: type 'EST' with a `trunk_id` field.
                    - `VoiceConfigurationDictFAX`: type 'FAX' with a `service_id` field.
            callback_url (StrictStr): The callback URL to receive notifications.
            **kwargs: Additional parameters for the request.

        Returns:
            RentAnyNumberRequest: A response object with the activated number and its details.

        For detailed documentation, visit https://developers.sinch.com
        """
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

    def check_availability(self, phone_number: StrictStr, **kwargs) -> CheckNumberAvailabilityResponse:
        """
        Enter a specific phone number to check availability.

        Args:
            phone_number (str): The phone number in E.164 format with leading +.
            **kwargs: Additional parameters for the request.

        Returns:
            CheckNumberAvailabilityResponse: A response object with the availability status of the number.

        For detailed documentation, visit https://developers.sinch.com
        """
        request_data = CheckNumberAvailabilityRequest(phone_number=phone_number, **kwargs)
        return self._request(SearchForNumberEndpoint, request_data)
