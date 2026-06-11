from enum import Enum
from abc import ABC, abstractmethod
import threading
from sinch.domains.authentication.models.v1.authentication import OAuthToken
from sinch.domains.authentication.endpoints.v1.oauth import OAuthEndpoint
from sinch.core.exceptions import ValidationException


class TokenState(Enum):
    """
    Lifecycle state of the cached OAuth token.
    """

    VALID = "VALID"
    """
    A usable token is currently cached.
    """
    INVALID = "INVALID"
    """
    No token has been obtained yet.
    """


class TokenManagerBase(ABC):
    """
    Base class for OAuth token managers.

    Holds the cached access token together with the lock that guards every
    token mutation.
    """

    def __init__(self, sinch):
        self.sinch = sinch
        self.token: OAuthToken | None = None
        self.token_state: TokenState = TokenState.INVALID
        self._lock: threading.Lock = threading.Lock()

    @abstractmethod
    def get_auth_token(self) -> OAuthToken:
        pass

    @abstractmethod
    def refresh_auth_token(self, used_token: str) -> OAuthToken:
        pass


    def set_auth_token(self, token: dict):
        """
        Sets the OAuth token and marks the token_state as VALID.

        :param token: The token fields.
        :type token: dict
        :raises ValidationException: If the fields do not match the OAuthToken structure.
        """
        try:
            self.token = OAuthToken(**token)
            self.token_state = TokenState.VALID
        except TypeError:
            raise ValidationException(
                "Invalid authentication token structure",
                is_from_server=False,
                response=None
            )
        
    def _fetch_new_token(self) -> OAuthToken:
        """
        Requests a new token from the OAuth endpoint and stores it as the current token.

        :returns: The freshly fetched token.
        :rtype: OAuthToken
        """
        self.token = self.sinch.configuration.transport.request(OAuthEndpoint())
        self.token_state = TokenState.VALID
        return self.token


class TokenManager(TokenManagerBase):
    """
    Thread-safe synchronous OAuth token manager.
    """

    def get_auth_token(self) -> OAuthToken:
        """
        Returns the stored token, fetching one on first use. Uses double-checked locking

        :returns: A valid OAuth token.
        :rtype: OAuthToken
        """
        if self.token is not None:
            return self.token
        
        with self._lock:
            if self.token is not None:
                return self.token
            return self._fetch_new_token()
        
    def refresh_auth_token(self, used_token: str) -> OAuthToken:
        """
        Renews the token after an expired-token 401, deduping concurrent renewals.

        :param used_token: The access token used by the request that received the 401.
        :type used_token: str
        :returns: A valid token.
        :rtype: OAuthToken
        """
        with self._lock:
            if self.token is not None and self.token.access_token != used_token:
                return self.token                  
            return self._fetch_new_token()
