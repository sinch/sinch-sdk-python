from enum import Enum
from abc import ABC, abstractmethod
from sinch.domains.authentication.models.v1.authentication import OAuthToken
from sinch.domains.authentication.endpoints.v1.oauth import OAuthEndpoint
from sinch.core.exceptions import ValidationException


class TokenState(Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    EXPIRED = "EXPIRED"


class TokenManagerBase(ABC):
    def __init__(self, sinch):
        self.sinch = sinch
        self.token = None
        self.token_state = TokenState.INVALID

    @abstractmethod
    def get_auth_token(self) -> OAuthToken:
        pass

    def invalidate_expired_token(self):
        self.token = None
        self.token_state = TokenState.EXPIRED

    def handle_invalid_token(self, http_response):
        if http_response.headers.get("www-authenticate") and "expired" in http_response.headers["www-authenticate"]:
            self.invalidate_expired_token()

    def set_auth_token(self, token) -> None:
        try:
            self.token = OAuthToken(**token)
            self.token_state = TokenState.VALID
        except TypeError:
            raise ValidationException(
                "Invalid authentication token structure",
                is_from_server=False,
                response=None
            )


class TokenManager(TokenManagerBase):
    def get_auth_token(self) -> OAuthToken:
        if self.token:
            return self.token

        self.token = self.sinch.configuration.transport.request(OAuthEndpoint())
        self.token_state = TokenState.VALID
        return self.token
