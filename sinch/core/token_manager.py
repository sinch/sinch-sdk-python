from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional

from sinch.domains.authentication.models.authentication import OAuthToken
from sinch.domains.authentication.endpoints.oauth import OAuthEndpoint
from sinch.core.exceptions import ValidationException
from sinch.core.clients.sinch_client_base import ClientBase
from sinch.core.models.http_response import HTTPResponse


class TokenState(Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    EXPIRED = "EXPIRED"


class TokenManagerBase(ABC):
    def __init__(self, sinch: ClientBase):
        self.sinch = sinch
        self.token: Optional[OAuthToken] = None
        self.token_state = TokenState.INVALID

    @abstractmethod
    def get_auth_token(self) -> Optional[OAuthToken]:
        pass

    def invalidate_expired_token(self):
        self.token = None
        self.token_state = TokenState.EXPIRED

    def handle_invalid_token(self, http_response: HTTPResponse):
        if http_response.headers.get("www-authenticate") and "expired" in http_response.headers["www-authenticate"]:
            self.invalidate_expired_token()

    def set_auth_token(self, token: dict) -> None:
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
    def get_auth_token(self) -> Optional[OAuthToken]:
        if self.token:
            return self.token

        self.token = self.sinch.configuration.transport.request(OAuthEndpoint())
        self.token_state = TokenState.VALID
        return self.token


class TokenManagerAsync(TokenManagerBase):
    async def get_auth_token(self) -> Optional[OAuthToken]:
        if self.token:
            return self.token

        self.token = await self.sinch.configuration.transport.request(OAuthEndpoint())
        self.token_state = TokenState.VALID
        return self.token
