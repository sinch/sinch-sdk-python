from logging import Logger
from typing import Union

from sinch.core.clients.retry_configuration import RetryConfiguration
from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.core.clients.transport_settings import TransportSettings
from sinch.core.enums import ConversationRegionEnum, SmsRegionEnum, VoiceRegionEnum
from sinch.core.token_manager import TokenManager
from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.domains.authentication import Authentication
from sinch.domains.numbers import VirtualNumbers
from sinch.domains.conversation import Conversation
from sinch.domains.sms import SMS
from sinch.domains.number_lookup import NumberLookup
from sinch.domains.voice import Voice


class SinchClient:
    """
    Synchronous implementation of the Sinch Client.

    By default it uses ``HTTPTransportRequests``, based on the ``requests`` library.
    A custom synchronous ``HTTPTransport`` can be assigned to ``configuration.transport``
    after initialization.

    :param key_id: Access key ID, used for OAuth authentication.
    :type key_id: str
    :param key_secret: Access key secret, used for OAuth authentication.
    :type key_secret: str
    :param project_id: Sinch project ID.
    :type project_id: str
    :param logger_name: Name of the logger to use. Takes precedence over ``logger``.
    :type logger_name: str
    :param logger: Logger instance to use. Defaults to the ``Sinch`` logger.
    :type logger: Logger
    :param service_plan_id: SMS service plan ID, used with ``sms_api_token``.
    :type service_plan_id: str
    :param sms_api_token: SMS API token, used with ``service_plan_id``.
    :type sms_api_token: str
    :param sms_region: SMS API region. Required when using the SMS API.
    :type sms_region: Union[SmsRegionEnum, str]
    :param conversation_region: Conversation API region. Required when using the Conversation API.
    :type conversation_region: Union[ConversationRegionEnum, str]
    :param voice_region: Voice API region. Defaults to the global endpoint.
    :type voice_region: Union[VoiceRegionEnum, str]
    :param transform_kwargs_casing: When
        ``True`` (default), extra fields on request/response models are
        auto-converted to the api convention ``snake_case`` or ``camelCase``, same as before 2.2.0.
        When ``False``, extra fields pass through unchanged in both
        directions.

        .. deprecated:: 2.2
            This flag is transitional and will be removed in 3.0, when extra fields will always pass
            through unchanged.
    :type transform_kwargs_casing: bool
    :param retry_configuration: Retry policy applied to rate-limited (HTTP 429) responses.
    :type retry_configuration: RetryConfiguration
    :param transport_settings: Transport level settings. When provided, its
        ``timeout_seconds`` replaces the default timeout of 10 seconds.
    :type transport_settings: TransportSettings
    """
    def __init__(
        self,
        key_id: str = None,
        key_secret: str = None,
        project_id: str = None,
        logger_name: str = None,
        logger: Logger = None,
        service_plan_id: str = None,
        sms_api_token: str = None,
        sms_region: Union[SmsRegionEnum, str] = None,
        conversation_region: Union[ConversationRegionEnum, str] = None,
        voice_region: Union[VoiceRegionEnum, str] = VoiceRegionEnum.GLOBAL,
        transform_kwargs_casing: bool = True,
        retry_configuration: RetryConfiguration = None,
        transport_settings: TransportSettings = None,
    ):
        self.configuration = Configuration(
            key_id=key_id,
            key_secret=key_secret,
            project_id=project_id,
            logger_name=logger_name,
            logger=logger,
            transport=HTTPTransportRequests(self),
            token_manager=TokenManager(self),
            service_plan_id=service_plan_id,
            sms_api_token=sms_api_token,
            sms_region=sms_region,
            conversation_region=conversation_region,
            voice_region=voice_region,
            transform_kwargs_casing=transform_kwargs_casing,
            retry_configuration=retry_configuration,
            transport_settings=transport_settings,
        )

        self.authentication = Authentication(self)
        self.numbers = VirtualNumbers(self)
        self.conversation = Conversation(self)
        self.sms = SMS(self)
        self.number_lookup = NumberLookup(self)
        self.voice = Voice(self)
