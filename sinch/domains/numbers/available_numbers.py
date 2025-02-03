from typing import Optional, TypedDict, overload, Literal, Union, Annotated
from typing_extensions import NotRequired
from pydantic import conlist, StrictInt, StrictStr, Field
from sinch.domains.numbers.endpoints.available.search_for_number import SearchForNumberEndpoint
from sinch.domains.numbers.endpoints.available.list_available_numbers import AvailableNumbersEndpoint
from sinch.domains.numbers.endpoints.available.activate_number import ActivateNumberEndpoint
from sinch.domains.numbers.endpoints.available.rent_any_number import RentAnyNumberEndpoint

from sinch.domains.numbers.models.available.list_available_numbers_request import ListAvailableNumbersRequest
from sinch.domains.numbers.models.available.activate_number_request import ActivateNumberRequest
from sinch.domains.numbers.models.available.check_number_availability_request import CheckNumberAvailabilityRequest
from sinch.domains.numbers.models.available.rent_any_number_request import RentAnyNumberRequest

from sinch.domains.numbers.models.available.list_available_numbers_response import ListAvailableNumbersResponse
from sinch.domains.numbers.models.available.activate_number_response import ActivateNumberResponse
from sinch.domains.numbers.models.available.check_number_availability_response import CheckNumberAvailabilityResponse
from sinch.domains.numbers.models.available.rent_any_number_response import RentAnyNumberResponse

# Define type aliases
NumberType = Union[Literal["MOBILE", "LOCAL", "TOLL_FREE"], StrictStr]
CapabilityType = conlist(Union[Literal["SMS", "VOICE"], StrictStr], min_length=1)
NumberSearchPatternType = Union[Literal["START", "CONTAINS", "END"], StrictStr]


class SmsConfigurationDict(TypedDict):
    service_plan_id: str
    campaign_id: NotRequired[str]


class VoiceConfigurationDictRTC(TypedDict):
    type: Literal["RTC"]
    app_id: NotRequired[str]


class VoiceConfigurationDictEST(TypedDict):
    type: Literal["EST"]
    trunk_id: NotRequired[str]


class VoiceConfigurationDictFAX(TypedDict):
    type: Literal["FAX"]
    service_id: NotRequired[str]


class VoiceConfigurationDictCustom(TypedDict):
    type: str


class NumberPatternDict(TypedDict):
    pattern: NotRequired[str]
    search_pattern: NotRequired[NumberSearchPatternType]


VoiceConfigurationDictType = Annotated[
    Union[VoiceConfigurationDictFAX, VoiceConfigurationDictRTC,
          VoiceConfigurationDictEST, VoiceConfigurationDictCustom],
    Field(discriminator="type")
]


class AvailableNumbers:
    def __init__(self, sinch):
        self._sinch = sinch

    def _request(self, endpoint_class, request_data):
        """
        A helper method to make requests to endpoints.

        Args:
            endpoint_class: The endpoint class to call.
            request_data: The request data to pass to the endpoint.

        Returns:
            The response from the Sinch transport request.
        """
        return self._sinch.configuration.transport.request(
            endpoint_class(
                project_id=self._sinch.configuration.project_id,
                request_data=request_data,
            )
        )

    def list(
        self,
        region_code: StrictStr,
        number_type: NumberType,
        number_pattern: Optional[StrictStr] = None,
        number_search_pattern: Optional[NumberSearchPatternType] = None,
        capabilities: Optional[CapabilityType] = None,
        page_size: Optional[StrictInt] = None,
        **kwargs
    ) -> ListAvailableNumbersResponse:
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
            ListAvailableNumbersResponse: A response object with available numbers and their details.

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
            sms_configuration: None,
            voice_configuration: None,
            callback_url: Optional[StrictStr] = None
    ) -> ActivateNumberResponse:
        pass

    @overload
    def activate(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictEST,
            callback_url: Optional[StrictStr] = None
    ) -> ActivateNumberResponse:
        pass

    @overload
    def activate(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictFAX,
            callback_url: Optional[StrictStr] = None
    ) -> ActivateNumberResponse:
        pass

    @overload
    def activate(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictRTC,
            callback_url: Optional[StrictStr] = None
    ) -> ActivateNumberResponse:
        pass

    def activate(
        self,
        phone_number: StrictStr,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDictType] = None,
        callback_url: Optional[StrictStr] = None,
        **kwargs
    ) -> ActivateNumberResponse:
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
            ActivateNumberResponse: A response object with the activated number and its details.

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
            type_: NumberType,
            sms_configuration: None,
            voice_configuration: None,
            number_pattern: Optional[NumberPatternDict] = None,
            capabilities: Optional[CapabilityType] = None,
            callback_url: Optional[str] = None,
    ) -> RentAnyNumberResponse:
        pass

    @overload
    def rent_any(
            self,
            region_code: StrictStr,
            type_: NumberType,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictRTC,
            number_pattern: Optional[NumberPatternDict] = None,
            capabilities: Optional[CapabilityType] = None,
            callback_url: Optional[str] = None,
    ) -> RentAnyNumberResponse:
        pass

    @overload
    def rent_any(
            self,
            region_code: StrictStr,
            type_: NumberType,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictFAX,
            number_pattern: Optional[NumberPatternDict] = None,
            capabilities: Optional[CapabilityType] = None,
            callback_url: Optional[str] = None,
    ) -> RentAnyNumberResponse:
        pass

    @overload
    def rent_any(
            self,
            region_code: StrictStr,
            type_: NumberType,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDictEST,
            number_pattern: Optional[NumberPatternDict] = None,
            capabilities: Optional[CapabilityType] = None,
            callback_url: Optional[str] = None,
    ) -> RentAnyNumberResponse:
        pass

    def rent_any(
        self,
        region_code: StrictStr,
        type_: NumberType,
        number_pattern: Optional[NumberPatternDict] = None,
        capabilities: Optional[CapabilityType] = None,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDictType] = None,
        callback_url: Optional[str] = None,
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
            callback_url (str): The callback URL to receive notifications.
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
