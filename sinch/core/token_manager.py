import warnings
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
    EXPIRED = "EXPIRED"
    """
    .. deprecated:: 2.1
        Kept for backward compatibility; will be removed in 3.0. No longer used
        by the SDK's own renewal path (see :meth:`TokenManager.refresh_auth_token`).
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
            token = self._request_token()
            self._set_valid_token(token)
            return token

    def invalidate_expired_token(self) -> None:
        """
        .. deprecated:: 2.1
            Token renewal is handled by :meth:`refresh_auth_token`; this method
            will be removed in 3.0.

        Clears the cached token so the next call fetches a new one.
        """
        warnings.warn(
            "TokenManagerBase.invalidate_expired_token() is deprecated and will be "
            "removed in 3.0. Token renewal is handled by refresh_auth_token().",
            DeprecationWarning,
            stacklevel=2,
        )
        self.token = None
        self.token_state = TokenState.EXPIRED

    def handle_invalid_token(self, http_response) -> None:
        """
        .. deprecated:: 2.1
            Expired-token handling now lives in the HTTP transport's request loop;
            this method will be removed in 3.0.

        Invalidates the cached token if the response signals an expired token.
        """
        warnings.warn(
            "TokenManagerBase.handle_invalid_token() is deprecated and will be "
            "removed in 3.0. Expired-token handling now lives in the transport.",
            DeprecationWarning,
            stacklevel=2,
        )
        www_authenticate = http_response.headers.get("www-authenticate") or ""
        if "expired" in www_authenticate:
            self.token = None
            self.token_state = TokenState.EXPIRED

    def set_auth_token(self, token: dict):
        """
        Sets the OAuth token and marks the token_state as VALID.

        :param token: The token fields.
        :type token: dict
        :raises ValidationException: If the fields do not match the OAuthToken structure.
        """
        try:
            self._set_valid_token(OAuthToken(**token))
        except TypeError:
            raise ValidationException(
                "Invalid authentication token structure",
                is_from_server=False,
                response=None
            )

    def _request_token(self) -> OAuthToken:
        """
        Requests a fresh token from the OAuth endpoint. No side effects.

        :returns: The freshly fetched token.
        :rtype: OAuthToken
        """
        return self.sinch.configuration.transport.request(OAuthEndpoint())

    def _set_valid_token(self, token: OAuthToken) -> None:
        """
        Caches the given token as the current valid one.

        :param token: The token to cache.
        :type token: OAuthToken
        """
        self.token = token
        self.token_state = TokenState.VALID


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
            token = self._request_token()
            self._set_valid_token(token)
            return token
