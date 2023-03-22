from sinch.core.clients.sinch_client_base import ClientBase
from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.core.token_manager import TokenManagerAsync
from sinch.core.adapters.asyncio_http_adapter import HTTPTransportAioHTTP
from sinch.domains.authentication import AuthenticationAsync
from sinch.domains.numbers import NumbersAsync
from sinch.domains.conversation import ConversationAsync
from sinch.domains.sms import SMSAsync


class ClientAsync(ClientBase):
    """
    Asynchronous implementation of the Sinch Client
    By default this implementation uses HTTPTransportAioHTTP based on AioHTTP library
    Custom Async HTTPTransport implementation can be provided via `transport` argument
    """
    def __init__(
        self,
        key_id,
        key_secret,
        project_id,
        logger_name=None,
        logger=None
    ):
        super().__init__(
            key_id=key_id,
            key_secret=key_secret,
            project_id=project_id,
            logger_name=logger_name,
            logger=logger
        )
        self.configuration = Configuration(
            key_id=key_id,
            key_secret=key_secret,
            project_id=project_id,
            logger_name=logger_name,
            logger=logger,
            transport=HTTPTransportAioHTTP(self),
            token_manager=TokenManagerAsync(self)
        )
        self.authentication = AuthenticationAsync(self)
        self.numbers = NumbersAsync(self)
        self.conversation = ConversationAsync(self)
        self.sms = SMSAsync(self)
