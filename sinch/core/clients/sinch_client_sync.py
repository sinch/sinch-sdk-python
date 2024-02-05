from typing import Optional
from logging import Logger
from sinch.core.clients.sinch_client_base import ClientBase
from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.core.token_manager import TokenManager
from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.domains.authentication import Authentication
from sinch.domains.numbers import Numbers
from sinch.domains.conversation import Conversation
from sinch.domains.sms import SMS
from sinch.domains.verification import Verification


class Client(ClientBase):
    """
    Synchronous implementation of the Sinch Client
    By default this implementation uses HTTPTransportRequests based on Requests library
    Custom Sync HTTPTransport implementation can be provided via `transport` argument
    """
    def __init__(
        self,
        key_id,
        key_secret,
        project_id,
        logger_name: Optional[str] = None,
        logger: Optional[Logger] = None,
        application_key: str = None,
        application_secret: str = None
    ):
        self.configuration = Configuration(
            key_id=key_id,
            key_secret=key_secret,
            project_id=project_id,
            logger_name=logger_name,
            logger=logger,
            transport=HTTPTransportRequests(self),
            token_manager=TokenManager(self),
            application_key=application_key,
            application_secret=application_secret
        )

        self.authentication = Authentication(self)
        self.numbers = Numbers(self)
        self.conversation = Conversation(self)
        self.sms = SMS(self)
        self.verification = Verification(self)
