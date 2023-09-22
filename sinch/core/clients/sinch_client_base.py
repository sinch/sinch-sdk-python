from abc import ABC
from sinch.core.exceptions import ValidationException
from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.domains.authentication import AuthenticationBase
from sinch.domains.numbers import NumbersBase
from sinch.domains.conversation import ConversationBase
from sinch.domains.sms import SMSBase
from typing import Optional
from logging import Logger


class ClientBase(ABC):
    """
    Sinch abstract base class for concrete Sinch Client implementations.
    By default this SDK provides two implementations - sync and async.
    Feel free to utilize any of them for you custom implementation.
    """
    def __init__(
        self,
        key_id: str,
        key_secret: str,
        project_id: str,
        logger_name: Optional[str]=None,
        logger: Optional[Logger]=None
    ):
        if not key_id or not key_secret or not project_id:
            raise ValidationException(
                message=(
                    "key_id, key_secret and project_id are required by the Sinch Client. "
                    "Those credentials can be obtained from Sinch portal."
                ),
                is_from_server=False,
                response=None
            )

        self.configuration = Configuration
        self.authentication = AuthenticationBase
        self.numbers = NumbersBase
        self.conversation = ConversationBase
        self.sms = SMSBase

    def __repr__(self):
        return f"Sinch SDK client for project_id: {self.configuration.project_id}"
