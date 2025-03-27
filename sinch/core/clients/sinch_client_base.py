from logging import Logger
from abc import ABC, abstractmethod
from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.domains.authentication import AuthenticationBase
from sinch.domains.numbers import NumbersBase
from sinch.domains.conversation import ConversationBase
from sinch.domains.sms import SMSBase
from sinch.domains.voice import VoiceBase


class SinchClientBase(ABC):
    """
    Sinch abstract base class for concrete Sinch Client implementation.
    Feel free to utilize any of them for you custom implementation.
    """
    configuration = Configuration
    authentication = AuthenticationBase
    numbers = NumbersBase
    conversation = ConversationBase
    sms = SMSBase
    voice = VoiceBase

    @abstractmethod
    def __init__(
        self,
        key_id: str = None,
        key_secret: str = None,
        project_id: str = None,
        logger_name: str = None,
        logger: Logger = None,
        application_key: str = None,
        application_secret: str = None,
        service_plan_id: str = None,
        sms_api_token: str = None
    ):
        pass

    def __repr__(self):
        return "Sinch SDK client"
