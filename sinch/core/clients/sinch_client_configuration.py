from logging import getLogger, Logger
from typing import Union, Optional

from sinch.core.ports.http_transport import HTTPTransport
from sinch.core.token_manager import TokenManager, TokenManagerAsync


class Configuration:
    """
    Sinch client configuration object.
    """
    def __init__(
        self,
        key_id: str,
        key_secret: str,
        project_id: str,
        transport: HTTPTransport,
        token_manager: Union[TokenManager, TokenManagerAsync],
        logger: Optional[Logger] = None,
        logger_name: Optional[str] = None,
        disable_https: bool = False,
        connection_timeout: int = 10
    ):
        self.key_id = key_id
        self.key_secret = key_secret
        self.project_id = project_id
        self.connection_timeout = connection_timeout
        self.auth_origin = "auth.sinch.com"
        self.numbers_origin = "numbers.api.sinch.com"
        self._conversation_region = "eu"
        self._conversation_domain = ".conversation.api.sinch.com"
        self._sms_region = "us"
        self._sms_domain = "zt.{}.sms.api.sinch.com"
        self._templates_region = "eu"
        self._templates_domain = ".template.api.sinch.com"
        self.token_manager = token_manager
        self.disable_https = disable_https
        self.transport: HTTPTransport = transport

        self._set_conversation_origin()
        self._set_sms_origin()
        self._set_templates_origin()

        if logger_name:
            self.logger = getLogger(logger_name)
        elif logger:
            self.logger = logger
        else:
            self.logger = getLogger("Sinch")

    def _set_sms_origin(self) -> None:
        self.sms_origin = self._sms_domain.format(self._sms_region)

    def _set_sms_region(self, region: str) -> None:
        self._sms_region = region
        self._set_sms_origin()

    def _get_sms_region(self) -> str:
        return self._sms_region

    sms_region = property(
        _get_sms_region,
        _set_sms_region,
        doc="SMS Region"
    )

    def _set_sms_domain(self, domain: str) -> None:
        self._sms_domain = domain
        self._set_sms_origin()

    def _get_sms_domain(self) -> None:
        return self.sms_domain

    sms_domain = property(
        _get_sms_domain,
        _set_sms_domain,
        doc="SMS Domain"
    )

    def _set_conversation_origin(self) -> None:
        self.conversation_origin = self._conversation_region + self._conversation_domain

    def _set_conversation_region(self, region: str) -> None:
        self._conversation_region = region
        self._set_conversation_origin()

    def _get_conversation_region(self) -> str:
        return self._conversation_region

    conversation_region = property(
        _get_conversation_region,
        _set_conversation_region,
        doc="ConversationAPI Region"
    )

    def _set_conversation_domain(self, domain: str) -> None:
        self._conversation_domain = domain
        self._set_conversation_origin()

    def _get_conversation_domain(self) -> str:
        return self._conversation_domain

    conversation_domain = property(
        _get_conversation_domain,
        _set_conversation_domain,
        doc="ConversationAPI Domain"
    )

    def _set_templates_origin(self) -> None:
        self.templates_origin = self._templates_region + self._templates_domain

    def _set_templates_region(self, region: str) -> None:
        self._templates_region = region
        self._set_templates_origin()

    def _get_templates_region(self) -> str:
        return self._templates_region

    templates_region = property(
        _get_templates_region,
        _set_templates_region,
        doc="Conversation API Templates Region"
    )

    def _set_templates_domain(self, domain: str) -> None:
        self._templates_domain = domain
        self._set_templates_origin()

    def _get_templates_domain(self) -> str:
        return self._templates_domain

    templates_domain = property(
        _get_templates_domain,
        _set_templates_domain,
        doc="Conversation API Templates Domain"
    )
