import logging
from logging import Logger
from typing import Union

from sinch.core.ports.http_transport import HTTPTransport
from sinch.core.token_manager import TokenManager, TokenManagerAsync
from sinch.core.enums import HTTPAuthentication


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
        logger: Logger = None,
        logger_name: str = None,
        connection_timeout=10,
        application_key: str = None,
        application_secret: str = None,
        service_plan_id: str = None,
        sms_api_token: str = None
    ):
        self.key_id = key_id
        self.key_secret = key_secret
        self.project_id = project_id
        self.application_key = application_key
        self.application_secret = application_secret
        self.connection_timeout = connection_timeout
        self.sms_api_token = sms_api_token
        self.service_plan_id = service_plan_id
        self.auth_origin = "auth.sinch.com"
        self.numbers_origin = "numbers.api.sinch.com"
        self.verification_origin = "verification.api.sinch.com"
        self.voice_applications_origin = "callingapi.sinch.com"
        self._voice_domain = "{}.api.sinch.com"
        self._voice_region = None
        self._conversation_region = "eu"
        self._conversation_domain = ".conversation.api.sinch.com"
        self._sms_region = "us"
        self._sms_region_with_service_plan_id = "us"
        self._sms_domain = "zt.{}.sms.api.sinch.com"
        self._sms_domain_with_service_plan_id = "{}.sms.api.sinch.com"
        self._sms_authentication = HTTPAuthentication.OAUTH.value
        self._templates_region = "eu"
        self._templates_domain = ".template.api.sinch.com"
        self.token_manager = token_manager
        self.transport: HTTPTransport = transport

        self._set_conversation_origin()
        self._set_sms_origin()
        self._set_sms_origin_with_service_plan_id()
        self._set_templates_origin()
        self._set_voice_origin()

        if logger_name:
            self.logger = logging.getLogger(logger_name)
        elif logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("Sinch")

    def _set_sms_origin_with_service_plan_id(self):
        self.sms_origin_with_service_plan_id = self._sms_domain_with_service_plan_id.format(
            self._sms_region_with_service_plan_id
        )

    def _set_sms_region_with_service_plan_id(self, region):
        self._sms_region_with_service_plan_id = region
        self._set_sms_origin_with_service_plan_id()

    def _get_sms_region_with_service_plan_id(self):
        return self._sms_region_with_service_plan_id

    sms_region_with_service_plan_id = property(
        _get_sms_region_with_service_plan_id,
        _set_sms_region_with_service_plan_id,
        doc="SMS Region for service plan id version of the SMS API"
    )

    def _set_sms_domain_with_service_plan_id(self, domain):
        self._sms_domain_with_service_plan_id = domain
        self._set_sms_origin_with_service_plan_id()

    def _get_sms_domain_with_service_plan_id(self):
        return self._sms_domain_with_service_plan_id

    sms_domain_with_service_plan_id = property(
        _get_sms_domain_with_service_plan_id,
        _set_sms_domain_with_service_plan_id,
        doc="SMS Domain for service plan id version of the SMS API"
    )

    def _set_sms_origin(self):
        self.sms_origin = self._sms_domain.format(self._sms_region)

    def _set_sms_region(self, region):
        self._sms_region = region
        self._set_sms_origin()

    def _get_sms_region(self):
        return self._sms_region

    sms_region = property(
        _get_sms_region,
        _set_sms_region,
        doc="SMS Region"
    )

    def _set_sms_domain(self, domain):
        self._sms_domain = domain
        self._set_sms_origin()

    def _get_sms_domain(self):
        return self._sms_domain

    sms_domain = property(
        _get_sms_domain,
        _set_sms_domain,
        doc="SMS Domain"
    )

    def _set_conversation_origin(self):
        self.conversation_origin = self._conversation_region + self._conversation_domain

    def _set_conversation_region(self, region):
        self._conversation_region = region
        self._set_conversation_origin()

    def _get_conversation_region(self):
        return self._conversation_region

    conversation_region = property(
        _get_conversation_region,
        _set_conversation_region,
        doc="ConversationAPI Region"
    )

    def _set_conversation_domain(self, domain):
        self._conversation_domain = domain
        self._set_conversation_origin()

    def _get_conversation_domain(self):
        return self._conversation_domain

    conversation_domain = property(
        _get_conversation_domain,
        _set_conversation_domain,
        doc="ConversationAPI Domain"
    )

    def _set_templates_origin(self):
        self.templates_origin = self._templates_region + self._templates_domain

    def _set_templates_region(self, region):
        self._templates_region = region
        self._set_templates_origin()

    def _get_templates_region(self):
        return self._templates_region

    templates_region = property(
        _get_templates_region,
        _set_templates_region,
        doc="Conversation API Templates Region"
    )

    def _set_templates_domain(self, domain):
        self._templates_domain = domain
        self._set_templates_origin()

    def _get_templates_domain(self):
        return self._templates_domain

    templates_domain = property(
        _get_templates_domain,
        _set_templates_domain,
        doc="Conversation API Templates Domain"
    )

    def _set_voice_origin(self):
        if not self._voice_region:
            self.voice_origin = self._voice_domain.format("calling")
        else:
            self.voice_origin = self._voice_domain.format("calling-" + self._voice_region)

    def _set_voice_region(self, region):
        self._voice_region = region
        self._set_voice_origin()

    def _get_voice_region(self):
        return self._voice_region

    voice_region = property(
        _get_voice_region,
        _set_voice_region,
        doc="Voice Region"
    )
