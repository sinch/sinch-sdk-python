from typing import Optional, TypedDict, overload
from typing_extensions import NotRequired
from pydantic import conlist, StrictInt, StrictStr
from sinch.domains.numbers.endpoints.available.search_for_number import SearchForNumberEndpoint
from sinch.domains.numbers.endpoints.available.list_available_numbers import AvailableNumbersEndpoint
from sinch.domains.numbers.endpoints.available.activate_number import ActivateNumberEndpoint
from sinch.domains.numbers.models.available.list_available_numbers_request import ListAvailableNumbersRequest
from sinch.domains.numbers.models.available.activate_number_request import ActivateNumberRequest
from sinch.domains.numbers.models.available.check_number_availability_request import CheckNumberAvailabilityRequest

from sinch.domains.numbers.models.available.list_available_numbers_response import ListAvailableNumbersResponse
from sinch.domains.numbers.models.available.activate_number_response import ActivateNumberResponse
from sinch.domains.numbers.models.available.check_number_availability_response import CheckNumberAvailabilityResponse


class SmsConfigurationDict(TypedDict):
    service_plan_id: str
    campaign_id: NotRequired[str]


class VoiceConfigurationDict(TypedDict):
    type: str
    app_id: NotRequired[str]


class NumberPatternDict(TypedDict):
    pattern: NotRequired[str]
    search_pattern: NotRequired[str]


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
        number_type: StrictStr,
        number_pattern: Optional[StrictStr] = None,
        number_search_pattern: Optional[StrictStr] = None,
        capabilities: Optional[conlist] = None,
        page_size: Optional[StrictInt] = None,
        **kwargs
    ) -> ListAvailableNumbersResponse:
        """
        Search for available virtual numbers for you to activate using a variety of parameters to filter results.

        Args:
            region_code (str): ISO 3166-1 alpha-2 country code of the phone number.
            number_type (str): Type of number (MOBILE, LOCAL, TOLL_FREE).
            number_pattern (str): Specific sequence of digits to search for.
            number_search_pattern (str): Pattern to apply (START, CONTAIN, END).
            capabilities (list): Capabilities (SMS, VOICE) required for the number.
            page_size (int): Maximum number of items to return.
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
            sms_configuration: None = None,
            voice_configuration: None = None,
            callback_url: Optional[StrictStr] = None
    ) -> ActivateNumberResponse:
        pass

    @overload
    def activate(
            self,
            phone_number: StrictStr,
            sms_configuration: SmsConfigurationDict,
            voice_configuration: VoiceConfigurationDict,
            callback_url: Optional[StrictStr] = None
    ) -> ActivateNumberResponse:
        pass

    def activate(
        self,
        phone_number: StrictStr,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDict] = None,
        callback_url: Optional[StrictStr] = None,
        **kwargs
    ) -> ActivateNumberResponse:
        """
        Activate a virtual number to use with SMS products, Voice products, or both.

        Args:
            phone_number (StrictStr): The phone number in E.164 format with leading +.
            sms_configuration (SmsConfigurationDict): Configuration for SMS activation.
            voice_configuration (VoiceConfigurationDict): Configuration for Voice activation.
            callback_url (StrictStr): The callback URL to be called.
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
