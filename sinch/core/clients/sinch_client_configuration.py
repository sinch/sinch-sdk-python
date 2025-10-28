import logging
from logging import Logger

from sinch.core.ports.http_transport import HTTPTransport
from sinch.core.token_manager import TokenManager
from sinch.core.enums import HTTPAuthentication


class Configuration:
    """
    Sinch client configuration object.
    """
    def __init__(
        self,
        transport: HTTPTransport,
        token_manager: TokenManager,
        connection_timeout=10,
        key_id: str = None,
        key_secret: str = None,
        project_id: str = None,
        logger: Logger = None,
        logger_name: str = None,
        application_key: str = None,
        application_secret: str = None,
        service_plan_id: str = None,
        sms_api_token: str = None,
        sms_region: str = None,
    ):
        self.key_id = key_id
        self.key_secret = key_secret
        self.project_id = project_id
        self.application_key = application_key
        self.application_secret = application_secret
        self.connection_timeout = connection_timeout
        self.sms_api_token = sms_api_token
        self.service_plan_id = service_plan_id
        
        # Determine authentication method based on provided parameters
        self._authentication_method = self._determine_authentication_method()
        self.auth_origin = "https://auth.sinch.com"
        self.numbers_origin = "https://numbers.api.sinch.com"
        self.verification_origin = "https://verification.api.sinch.com"
        self.voice_applications_origin = "https://callingapi.sinch.com"
        self._voice_domain = "https://{}.api.sinch.com"
        self._voice_region = None
        self._conversation_region = "eu"
        self._conversation_domain = ".conversation.api.sinch.com"
        self._sms_region = sms_region
        self._sms_region_with_service_plan_id = sms_region
        self._sms_domain = "https://zt.{}.sms.api.sinch.com"
        self._sms_domain_with_service_plan_id = "https://{}.sms.api.sinch.com"
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
        if self._sms_region_with_service_plan_id:
            self.sms_origin_with_service_plan_id = self._sms_domain_with_service_plan_id.format(
                self._sms_region_with_service_plan_id
            )
        else:
            self.sms_origin_with_service_plan_id = None

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
        if self._sms_region:
            self.sms_origin = self._sms_domain.format(self._sms_region)
        else:
            self.sms_origin = None

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

    def _determine_authentication_method(self):
        """
        Determines the authentication method based on provided parameters.
        Priority: SMS authentication (service_plan_id + sms_api_token) over project authentication (project_id).
        """
        if self.service_plan_id and self.sms_api_token:
            return "sms_auth"
        elif self.project_id:
            return "project_auth"
        else:
            # No authentication parameters provided - will be validated later
            return None

    @property
    def authentication_method(self):
        """Returns the determined authentication method"""
        return self._authentication_method

    def validate_authentication_parameters(self):
        """
        Validates that sufficient authentication parameters are provided.
        This should be called before making actual API requests.
        """
        # Check for incomplete SMS auth only if not using project auth
        # This prevents false positives when both service_plan_id and project_id are provided
        has_project_auth = self.project_id and self.key_id and self.key_secret
        if self.service_plan_id and not self.sms_api_token and not has_project_auth:
            raise ValueError(
                "The sms_api_token is required when using service_plan_id"
            )
        if self._authentication_method is None or self._authentication_method == "project_auth":
            # Default to project_auth and validate parameters
            if not self.project_id:
                raise ValueError(
                    "The project_id is required"
                )
            if not self.key_id or not self.key_secret:
                raise ValueError(
                    "The key_id and key_secret are required"
                )
        elif self._authentication_method == "sms_auth":
            if not self.service_plan_id or not self.sms_api_token:
                raise ValueError(
                    "The service_plan_id and sms_api_token are required"
                )

    def get_sms_origin_for_auth(self):
        """
        Returns the appropriate SMS origin based on the authentication method.
        - SMS auth (service_plan_id + sms_api_token): uses sms_origin_with_service_plan_id
        - Project auth (project_id): uses regular sms_origin
        """
        if self._authentication_method == "sms_auth":
            return self.sms_origin_with_service_plan_id
        else:
            return self.sms_origin
