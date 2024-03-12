from logging import Logger
from sinch.core.clients.sinch_client_base import ClientBase
from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.core.token_manager import TokenManagerAsync
from sinch.core.adapters.asyncio_http_adapter import HTTPTransportAioHTTP
from sinch.domains.authentication import AuthenticationAsync
from sinch.domains.numbers import NumbersAsync
from sinch.domains.conversation import ConversationAsync
from sinch.domains.sms import SMSAsync
from sinch.domains.verification import Verification as VerificationAsync


class ClientAsync(ClientBase):
    """
    Asynchronous implementation of the Sinch Client
    By default this implementation uses HTTPTransportAioHTTP based on AioHTTP library
    Custom Async HTTPTransport implementation can be provided via `transport` argument
    """
    def __init__(
        self,
        key_id: str = None,
        key_secret: str = None,
        project_id: str = None,
        logger_name: str = None,
        logger: Logger = None,
        application_key: str = None,
        application_secret: str = None
    ):
        self.configuration = Configuration(
            key_id=key_id,
            key_secret=key_secret,
            project_id=project_id,
            logger_name=logger_name,
            logger=logger,
            transport=HTTPTransportAioHTTP(self),
            token_manager=TokenManagerAsync(self),
            application_secret=application_secret,
            application_key=application_key
        )

        self.authentication = AuthenticationAsync(self)
        self.numbers = NumbersAsync(self)
        self.conversation = ConversationAsync(self)
        self.sms = SMSAsync(self)
        self.verification = VerificationAsync(self)
