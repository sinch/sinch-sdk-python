from typing import Optional
from sinch.domains.numbers.endpoints.available.search_for_number import SearchForNumberEndpoint
from sinch.domains.numbers.endpoints.available.list_available_numbers import AvailableNumbersEndpoint
from sinch.domains.numbers.endpoints.available.activate_number import ActivateNumberEndpoint
from sinch.domains.numbers.endpoints.available.rent_any_number import RentAnyNumberEndpoint
from sinch.domains.numbers.models.available.requests import (
    ListAvailableNumbersRequest, ActivateNumberRequest,
    CheckNumberAvailabilityRequest, RentAnyNumberRequest
)
from sinch.domains.numbers.models.available.responses import (
    ListAvailableNumbersResponse, ActivateNumberResponse,
    CheckNumberAvailabilityResponse
)


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
        region_code: str,
        number_type: str,
        number_pattern: Optional[str] = None,
        number_search_pattern: Optional[str] = None,
        capabilities: Optional[list] = None,
        page_size: Optional[int] = None,
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

    def activate(
        self,
        phone_number: str,
        sms_configuration: Optional[dict] = None,
        voice_configuration: Optional[dict] = None,
        **kwargs
    ) -> ActivateNumberResponse:
        """
        Activate a virtual number to use with SMS products, Voice products, or both.

        Args:
            phone_number (str): The phone number in E.164 format with leading +.
            sms_configuration (dict): Configuration for SMS activation.
            voice_configuration (dict): Configuration for Voice activation.
            **kwargs: Additional parameters for the request.

        Returns:
            ActivateNumberResponse: A response object with the activated number and its details.

        For detailed documentation, visit https://developers.sinch.com
        """
        request_data = ActivateNumberRequest(
            phone_number=phone_number,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            **kwargs
        )
        return self._request(ActivateNumberEndpoint, request_data)

    def rent_any(
        self,
        region_code: str,
        type_: str,
        number_pattern: Optional[str] = None,
        capabilities: Optional[list] = None,
        sms_configuration: Optional[dict] = None,
        voice_configuration: Optional[dict] = None,
        callback_url: Optional[str] = None,
        **kwargs
    ) -> RentAnyNumberRequest:
        """
        Search for and activate an available Sinch virtual number all in one API call.
        Currently, the rentAny operation works only for US 10DLC numbers

        Args:
            region_code (str): ISO 3166-1 alpha-2 country code of the phone number.
            type_ (str): Type of number (MOBILE, LOCAL, TOLL_FREE).
            number_pattern (str): Specific sequence of digits to search for.
            capabilities (list): Capabilities (SMS, VOICE) required for the number.
            sms_configuration (dict): Configuration for SMS activation.
            voice_configuration (dict): Configuration for Voice activation.
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

    def check_availability(self, phone_number: str, **kwargs) -> CheckNumberAvailabilityResponse:
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
