from logging import Logger
from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.core.token_manager import TokenManager
from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.domains.authentication import Authentication
from sinch.domains.numbers import VirtualNumbers
from sinch.domains.conversation import Conversation
from sinch.domains.sms import SMS
from sinch.domains.number_lookup import NumberLookup


class SinchClient:
    """
    Synchronous implementation of the Sinch Client
    By default this implementation uses HTTPTransportRequests based on Requests library
    Custom Sync HTTPTransport implementation can be provided via `transport` argument

    :param transform_kwargs_casing: When
        ``True`` (default), extra fields on request/response models are
        auto-converted to the api convention ``snake_case`` or ``camelCase``, same as before 2.2.0.
        When ``False``, extra fields pass through unchanged in both
        directions.

        .. deprecated:: 2.2
            This flag is transitional and will be removed in 3.0, when extra fields will always pass
            through unchanged.
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
        sms_region: str = None,
        conversation_region: str = None,
        transform_kwargs_casing: bool = True,
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
            transform_kwargs_casing=transform_kwargs_casing,
        )

        self.authentication = Authentication(self)
        self.numbers = VirtualNumbers(self)
        self.conversation = Conversation(self)
        self.sms = SMS(self)
        self.number_lookup = NumberLookup(self)
