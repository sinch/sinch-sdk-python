from typing import Optional, overload, List
from sinch.domains.numbers.api.v1 import (
    ActiveNumbers, AvailableNumbers, AvailableRegions, CallbackConfiguration
)
from sinch.core.pagination import Paginator
from sinch.domains.numbers.models.v1.response import (
    ActiveNumber, AvailableNumber
)
from sinch.domains.numbers.models.v1.types import (
    CapabilityType, NumberSearchPatternType, NumberType, OrderBy,
    SmsConfigurationDict, VoiceConfigurationDict, VoiceConfigurationFAXDict, VoiceConfigurationRTCDict,
    VoiceConfigurationESTDict, NumberPatternDict
)
from sinch.domains.numbers.webhooks.v1 import NumbersWebhooks


class VirtualNumbers:
    """
    Synchronous version of the Numbers domain.

    Documentation for Sinch virtual Numbers is found at
    https://developers.sinch.com/docs/numbers/.
    """

    def __init__(self, sinch):
        self._sinch = sinch
        self.regions = AvailableRegions(self._sinch)
        self.callback_configuration = CallbackConfiguration(self._sinch)

        self._active = ActiveNumbers(self._sinch)
        self._available = AvailableNumbers(self._sinch)

    def webhooks(self, callback_secret: str) -> NumbersWebhooks:
        """
        Create a Numbers webhooks handler with the specified callback secret.

        :param callback_secret: Secret used for webhook validation.
        :type callback_secret: str
        :returns: A configured webhooks handler
        :rtype: NumbersWebhooks
        """
        return NumbersWebhooks(callback_secret)

    # ====== High-Level Convenience Methods ======

    def list(
        self,
        region_code: str,
        number_type: NumberType,
        number_pattern: Optional[str] = None,
        number_search_pattern: Optional[NumberSearchPatternType] = None,
        capabilities: Optional[List[CapabilityType]] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        order_by: Optional[OrderBy] = None,
        **kwargs
    ) -> Paginator[ActiveNumber]:
        """
        Search for all active virtual numbers associated with a certain project.

        :param region_code: ISO 3166-1 alpha-2 country code of the phone number.
        :type region_code: str

        :param number_type: Type of number (e.g., "MOBILE", "LOCAL", "TOLL_FREE").
        :type number_type: NumberType

        :param number_pattern: Specific sequence of digits to search for.
        :type number_pattern: Optional[str]

        :param number_search_pattern: Pattern to apply (e.g., "START", "CONTAINS", "END").
        :type number_search_pattern: Optional[NumberSearchPatternType]

        :param capabilities: Capabilities required for the number (e.g., ["SMS", "VOICE"]).
        :type capabilities: Optional[List[CapabilityType]]

        :param page_size: Maximum number of items to return.
        :type page_size: int

        :param page_token: Token for the next page of results.
        :type page_token: Optional[str]

        :param order_by: Field to order the results by (e.g., "phoneNumber", "displayName").
        :type order_by: Optional[OrderBy]

        :param kwargs: Additional filters for the request.
        :type kwargs: dict

        :returns: A paginator for iterating through the results.
        :rtype: Paginator[ActiveNumber]

        For detailed documentation, visit https://developers.sinch.com
        """
        return self._active.list(
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

    @overload
    def update(
        self,
        phone_number: str,
        sms_configuration: SmsConfigurationDict,
        voice_configuration: VoiceConfigurationESTDict,
        display_name: Optional[str] = None,
        callback_url: Optional[str] = None
    ) -> ActiveNumber:
        pass

    @overload
    def update(
        self,
        phone_number: str,
        sms_configuration: SmsConfigurationDict,
        voice_configuration: VoiceConfigurationFAXDict,
        display_name: Optional[str] = None,
        callback_url: Optional[str] = None
    ) -> ActiveNumber:
        pass

    @overload
    def update(
        self,
        phone_number: str,
        sms_configuration: SmsConfigurationDict,
        voice_configuration: VoiceConfigurationRTCDict,
        display_name: Optional[str] = None,
        callback_url: Optional[str] = None
    ) -> ActiveNumber:
        pass

    def update(
        self,
        phone_number: str,
        display_name: Optional[str] = None,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDict] = None,
        callback_url: Optional[str] = None,
        **kwargs
    ) -> ActiveNumber:
        """
        Make updates to the configuration of your virtual number.
        Update the display name, change the currency type, or reconfigure for either SMS and/or Voice.

        :param phone_number: The phone number in E.164 format with leading +.
        :type phone_number: str

        :param display_name: The display name for the virtual number.
        :type display_name: Optional[str]

        :param sms_configuration: A dictionary defining the SMS configuration. Including fields such as::

                                  - ``service_plan_id`` (str): The service plan ID.
                                  - ``campaign_id`` (Optional[str]): The campaign ID.
        :type sms_configuration: Optional[SmsConfigurationDict]

        :param voice_configuration: A dictionary defining the Voice configuration. Supported types include::

                                    - ``VoiceConfigurationRTCDict``: type 'RTC' with an ``app_id`` field.
                                    - ``VoiceConfigurationESTDict``: type 'EST' with a ``trunk_id`` field.
                                    - ``VoiceConfigurationFAXDict``: type 'FAX' with a ``service_id`` field.
        :type voice_configuration: Optional[VoiceConfigurationDict]

        :param callback_url: The callback URL for the virtual number.
        :type callback_url: Optional[str]

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        For detailed documentation, visit https://developers.sinch.com
        """
        return self._active.update(
            phone_number=phone_number,
            display_name=display_name,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            callback_url=callback_url,
            **kwargs
        )

    def get(
        self,
        phone_number: str,
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
        return self._active.get(phone_number=phone_number, **kwargs)

    def release(
        self,
        phone_number: str,
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
        return self._active.release(phone_number=phone_number, **kwargs)

    def check_availability(self, phone_number: str, **kwargs) -> AvailableNumber:
        """
        Enter a specific phone number to check availability.

        :param phone_number: The phone number in E.164 format with leading ``+``.
        :type phone_number: str

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: A response object with the availability status of the number.
        :rtype: AvailableNumber

        For detailed documentation, visit: https://developers.sinch.com
        """
        return self._available.check_availability(phone_number=phone_number, **kwargs)

    @overload
    def rent(
        self,
        phone_number: str,
        sms_configuration: SmsConfigurationDict,
        voice_configuration: VoiceConfigurationESTDict,
        callback_url: Optional[str] = None
    ) -> ActiveNumber:
        pass

    @overload
    def rent(
        self,
        phone_number: str,
        sms_configuration: SmsConfigurationDict,
        voice_configuration: VoiceConfigurationFAXDict,
        callback_url: Optional[str] = None
    ) -> ActiveNumber:
        pass

    @overload
    def rent(
        self,
        phone_number: str,
        sms_configuration: SmsConfigurationDict,
        voice_configuration: VoiceConfigurationRTCDict,
        callback_url: Optional[str] = None
    ) -> ActiveNumber:
        pass

    def rent(
        self,
        phone_number: str,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDict] = None,
        callback_url: Optional[str] = None,
        **kwargs
    ) -> ActiveNumber:
        """
        Rent a virtual number to use with SMS, Voice, or both products.

        :param phone_number: The phone number in E.164 format with leading ``+``.
        :type phone_number: str
        :param sms_configuration: A dictionary defining the SMS configuration.
            Include the following fields::

            - ``service_plan_id`` (str): The service plan ID.
            - ``campaign_id`` (Optional[str]): The campaign ID.
        :type sms_configuration: Optional[SmsConfigurationDict]
        :param voice_configuration: A dictionary defining the Voice configuration. Supported types include::

            - ``VoiceConfigurationRTCDict``: type ``'RTC'`` with an ``app_id`` field.
            - ``VoiceConfigurationESTDict``: type ``'EST'`` with a ``trunk_id`` field.
            - ``VoiceConfigurationFAXDict``: type ``'FAX'`` with a ``service_id`` field.
        :type voice_configuration: Optional[VoiceConfigurationDict]
        :param callback_url: The callback URL to be called.
        :type callback_url: Optional[str]
        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: A response object with the rented number and its details.
        :rtype: ActiveNumber

        For detailed documentation, visit https://developers.sinch.com
        """
        return self._available.rent(
            phone_number=phone_number,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            callback_url=callback_url,
            **kwargs
        )

    @overload
    def rent_any(
        self,
        region_code: str,
        number_type: NumberType,
        sms_configuration: SmsConfigurationDict,
        voice_configuration: VoiceConfigurationRTCDict,
        number_pattern: NumberPatternDict,
        capabilities: Optional[CapabilityType] = None,
        callback_url: Optional[str] = None
    ) -> ActiveNumber:
        pass

    @overload
    def rent_any(
        self,
        region_code: str,
        number_type: NumberType,
        sms_configuration: SmsConfigurationDict,
        voice_configuration: VoiceConfigurationFAXDict,
        number_pattern: NumberPatternDict,
        capabilities: Optional[List[CapabilityType]] = None,
        callback_url: Optional[str] = None
    ) -> ActiveNumber:
        pass

    @overload
    def rent_any(
        self,
        region_code: str,
        number_type: NumberType,
        sms_configuration: SmsConfigurationDict,
        voice_configuration: VoiceConfigurationESTDict,
        number_pattern: NumberPatternDict,
        capabilities: Optional[List[CapabilityType]] = None,
        callback_url: Optional[str] = None
    ) -> ActiveNumber:
        pass

    def rent_any(
        self,
        region_code: str,
        number_type: NumberType,
        number_pattern: Optional[NumberPatternDict] = None,
        capabilities: Optional[List[CapabilityType]] = None,
        sms_configuration: Optional[SmsConfigurationDict] = None,
        voice_configuration: Optional[VoiceConfigurationDict] = None,
        callback_url: Optional[str] = None,
        **kwargs
    ) -> ActiveNumber:
        """
        Search for and activate an available Sinch virtual number all in one API call.
        Currently, the ``rent_any`` operation works only for US 10DLC numbers.

        :param region_code: ISO 3166-1 alpha-2 country code of the phone number.
        :type region_code: str

        :param number_type: Type of number (e.g., ``"MOBILE"``, ``"LOCAL"``, ``"TOLL_FREE"``). Defaults to ``"MOBILE"``.
        :type number_type: NumberType

        :param number_pattern: A dictionary defining the specific sequence of digits to search for.
        Include fields such as::
                                    - ``pattern`` (str): The specific sequence of digits.
                                    - ``search_pattern`` (str):
                                            The pattern to apply (e.g., ``"START"``, ``"CONTAINS"``, ``"END"``).
        :type number_pattern: Optional[NumberPatternDict]

        :param capabilities: Capabilities required for the number (e.g., ``["SMS", "VOICE"]``).
        :type capabilities: Optional[CapabilityType]

        :param sms_configuration: A dictionary defining the SMS configuration. Includes fields such as::

                                  - ``service_plan_id`` (str): The service plan ID.
                                  - ``campaign_id`` (Optional[str]): The campaign ID.
        :type sms_configuration: Optional[SmsConfigurationDict]

        :param voice_configuration: A dictionary defining the Voice configuration. Supported types include::

                                   - ``VoiceConfigurationRTCDict``: type ``'RTC'`` with an ``app_id`` field.
                                   - ``VoiceConfigurationESTDict``: type ``'EST'`` with a ``trunk_id`` field.
                                   - ``VoiceConfigurationFAXDict``: type ``'FAX'`` with a ``service_id`` field.
        :type voice_configuration: Optional[VoiceConfigurationDict]

        :param callback_url: The callback URL to receive notifications.
        :type callback_url: str

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: A response object with the activated number and its details.
        :rtype: RentAnyNumberRequest

        For detailed documentation, visit: https://developers.sinch.com
        """
        return self._available.rent_any(
            region_code=region_code,
            number_type=number_type,
            number_pattern=number_pattern,
            capabilities=capabilities,
            sms_configuration=sms_configuration,
            voice_configuration=voice_configuration,
            callback_url=callback_url,
            **kwargs
        )

    def search_for_available_numbers(
        self,
        region_code: str,
        number_type: NumberType,
        number_pattern: Optional[str] = None,
        number_search_pattern: Optional[NumberSearchPatternType] = None,
        capabilities: Optional[List[CapabilityType]] = None,
        page_size: Optional[int] = None,
        **kwargs
    ) -> Paginator[AvailableNumber]:
        """
        Search for available virtual numbers for you to rent using a variety of parameters to filter results.

        :param region_code: ISO 3166-1 alpha-2 country code of the phone number.
        :type region_code: str

        :param number_type: Type of number (e.g., ``"MOBILE"``, ``"LOCAL"``, ``"TOLL_FREE"``).
        :type number_type: NumberType

        :param number_pattern: Specific sequence of digits to search for.
        :type number_pattern: Optional[str]

        :param number_search_pattern: Pattern to apply (e.g., ``"START"``, ``"CONTAINS"``, ``"END"``).
        :type number_search_pattern: Optional[NumberSearchPatternType]

        :param capabilities: Capabilities required for the number (e.g., ``["SMS", "VOICE"]``).
        :type capabilities: Optional[List[CapabilityType]]

        :param page_size: Maximum number of items to return.
        :type page_size: int

        :param kwargs: Additional filters for the request.
        :type kwargs: dict

        :returns: A paginator for iterating through the results.
        :rtype: Paginator[AvailableNumber]

        For detailed documentation, visit: https://developers.sinch.com
        """
        return self._available.search_for_available_numbers(
            region_code=region_code,
            number_type=number_type,
            page_size=page_size,
            capabilities=capabilities,
            number_pattern=number_pattern,
            number_search_pattern=number_search_pattern,
            **kwargs
        )
