from abc import ABC, abstractmethod
from platform import python_version
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.exceptions import ValidationException, SinchException
from sinch.core.enums import HTTPAuthentication
from sinch.core.token_manager import TokenState
from sinch import __version__ as sdk_version


class HTTPTransport(ABC):
    """Base class for HTTP transports.

    Subclasses implement ``send`` to perform the raw HTTP call.
    The public ``request`` method adds cross-cutting concerns on top:
    authentication, logging hooks, and automatic token refresh on 401.
    """

    def __init__(self, sinch):
        self.sinch = sinch

    # ------------------------------------------------------------------
    # Subclass contract
    # ------------------------------------------------------------------

    @abstractmethod
    def send(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        """Execute a single HTTP round-trip and return the response.

        Implementations must prepare the request, authenticate, perform the
        HTTP call, deserialize the response, and return an ``HTTPResponse``.
        They should **not** handle token refresh — that is done by
        ``request``.
        """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        """Send a request with automatic OAuth token refresh on 401.

        If the server responds with 401 *and* the token is detected as
        expired, the token is invalidated and **one** retry is attempted
        with a fresh token.  A second consecutive 401 is handed straight
        to the endpoint's error handler — no further retries.
        """
        http_response = self.send(endpoint)

        if self._should_refresh_token(endpoint, http_response):
            self.sinch.configuration.token_manager.handle_invalid_token(
                http_response
            )
            if (
                self.sinch.configuration.token_manager.token_state
                == TokenState.EXPIRED
            ):
                http_response = self.send(endpoint)

        return endpoint.handle_response(http_response)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def authenticate(self, endpoint, request_data):
        if endpoint.HTTP_AUTHENTICATION in (HTTPAuthentication.BASIC.value, HTTPAuthentication.OAUTH.value):
            if (
                not self.sinch.configuration.key_id
                or not self.sinch.configuration.key_secret
                or not self.sinch.configuration.project_id
            ):
                raise ValidationException(
                    message=(
                        "key_id, key_secret and project_id are required by this API. "
                        "Those credentials can be obtained from Sinch portal."
                    ),
                    is_from_server=False,
                    response=None
                )

        if endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.BASIC.value:
            request_data.auth = (self.sinch.configuration.key_id, self.sinch.configuration.key_secret)
        else:
            request_data.auth = None

        if endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.OAUTH.value:
            token = self.sinch.authentication.get_auth_token().access_token
            request_data.headers.update({
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
        elif endpoint.HTTP_AUTHENTICATION == HTTPAuthentication.SMS_TOKEN.value:
            if not self.sinch.configuration.sms_api_token or not self.sinch.configuration.service_plan_id:
                raise ValidationException(
                    message=(
                        "sms_api_token and service_plan_id are required by this API. "
                        "Those credentials can be obtained from Sinch portal."
                    ),
                    is_from_server=False,
                    response=None
                )
            request_data.headers.update({
                "Authorization": f"Bearer {self.sinch.configuration.sms_api_token}",
                "Content-Type": "application/json"
            })

        return request_data

    def prepare_request(self, endpoint: HTTPEndpoint) -> HttpRequest:
        url_query_params = endpoint.build_query_params()

        return HttpRequest(
            headers={
                "User-Agent": f"sinch-sdk/{sdk_version} (Python/{python_version()};"
                              f" {self.__class__.__name__};)"
            },
            url=endpoint.build_url(self.sinch),
            http_method=endpoint.HTTP_METHOD,
            request_body=endpoint.request_body(),
            query_params=url_query_params,
            auth=()
        )

    @staticmethod
    def deserialize_json_response(response):
        if response.content:
            try:
                response_body = response.json()
            except ValueError as err:
                raise SinchException(
                    message=f"Error while parsing json response. {err}",
                    is_from_server=True,
                    response=response
                )
        else:
            response_body = {}

        return response_body

    @staticmethod
    def _should_refresh_token(endpoint, http_response):
        """Return True when a 401 response should trigger a token refresh."""
        return (
            http_response.status_code == 401
            and endpoint.HTTP_AUTHENTICATION
            == HTTPAuthentication.OAUTH.value
        )
