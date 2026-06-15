import warnings
from abc import ABC
from platform import python_version
from typing import Optional

from requests import Response
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.models.http_request import HttpRequest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.exceptions import ValidationException, SinchException
from sinch.core.enums import HTTPAuthentication
from sinch import __version__ as sdk_version


class HTTPTransport(ABC):
    """
    Base class for HTTP transports.

    Subclasses implement :meth:`send_request` to perform the raw HTTP call. The public
    :meth:`request` method adds cross-cutting concerns on top: request
    preparation, authentication, and automatic token refresh on 401.

    .. deprecated:: 2.1
        Overriding :meth:`send` (the old ``send(endpoint)`` hook) is still
        honored but deprecated; implement :meth:`send_request` instead. The
        ``send`` override path will be removed in 3.0.
    """

    def __init__(self, sinch):
        self.sinch = sinch
        self._legacy_send = self._uses_legacy_send()
        if self._legacy_send:
            warnings.warn(
                f"{type(self).__name__} overrides `send(endpoint)`, which is deprecated and "
                "will be removed in 3.0. Implement `send_request(request_data)` instead.",
                DeprecationWarning,
                stacklevel=2,
            )

    def send_request(self, request_data: HttpRequest) -> HTTPResponse:
        """
        Performs a single HTTP round-trip for an already-prepared, authenticated request.

        :param request_data: The prepared request to send.
        :type request_data: HttpRequest
        :returns: The HTTP response.
        :rtype: HTTPResponse
        """
        raise NotImplementedError(
            "Transport subclasses must implement `send_request(request_data)`."
        )
    
    def send(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        """
        Prepares, authenticates and performs a single round-trip for an endpoint.

        .. deprecated:: 2.1
            This hook is deprecated. Implement :meth:`send_request` instead;
            the ``send`` override path will be removed in 3.0.

        :param endpoint: The endpoint to call.
        :type endpoint: HTTPEndpoint
        :returns: The HTTP response.
        :rtype: HTTPResponse
        """
        raise NotImplementedError(
            "`send(endpoint)` is deprecated. "
            "Implement `send_request(request_data)` instead."
        )
    
    def _uses_legacy_send(self) -> bool:
        """
        Returns True when a subclass overrides the deprecated ``send`` hook but
        not the new ``send_request`` hook.
        """
        cls = type(self)
        return cls.send is not HTTPTransport.send and cls.send_request is HTTPTransport.send_request


    def request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        """
        Sends a request, renewing the token and retrying once on an expired-token 401.

        :param endpoint: The endpoint to call.
        :type endpoint: HTTPEndpoint
        :returns: The handled HTTP response.
        :rtype: HTTPResponse
        """
        if self._legacy_send:
            return self._legacy_request(endpoint)

        request_data = self.prepare_request(endpoint)
        request_data = self.authenticate(endpoint, request_data)
        http_response = self.send_request(request_data)

        if self._should_refresh_token(endpoint, http_response):
            used_token = self._get_bearer_token_from_request(request_data)
            new_token = self.sinch.configuration.token_manager.refresh_auth_token(used_token)
            self._set_bearer_token(request_data, new_token.access_token)
            http_response = self.send_request(request_data)

        return endpoint.handle_response(http_response)


    def authenticate(self, endpoint: HTTPEndpoint, request_data: HttpRequest) -> HttpRequest:
        """
        Stamps the credentials required by the endpoint's auth scheme onto the request.

        :param endpoint: The endpoint being called, whose HTTP_AUTHENTICATION selects the scheme.
        :type endpoint: HTTPEndpoint
        :param request_data: The request to authenticate, mutated in place.
        :type request_data: HttpRequest
        :returns: The same request, with auth applied.
        :rtype: HttpRequest
        :raises ValidationException: If the credentials required by the scheme are missing.
        """
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
            self._set_bearer_token(request_data, token)
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
            self._set_bearer_token(request_data, self.sinch.configuration.sms_api_token)

        return request_data

    def prepare_request(self, endpoint: HTTPEndpoint) -> HttpRequest:
        """
        Builds the HttpRequest for an endpoint.

        :param endpoint: The endpoint to build the request for.
        :type endpoint: HTTPEndpoint
        :returns: The prepared request.
        :rtype: HttpRequest
        """
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
    def deserialize_json_response(response: Response) -> dict:
        """
        Parses the JSON body of a response.

        :param response: The raw HTTP response.
        :type response: Response
        :returns: The parsed body.
        :rtype: dict
        :raises SinchException: If the body is present but not valid JSON.
        """
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
    
    def _legacy_request(self, endpoint: HTTPEndpoint) -> HTTPResponse:
        """
        Backward-compatible request loop for subclasses that override ``send``.

        On an expired-token 401 the cached token is renewed through
        :meth:`TokenManagerBase.refresh_auth_token`, which dedupes concurrent
        renewals. The legacy ``send(endpoint)`` re-prepares and re-authenticates
        on every call, so the second ``send`` picks up the refreshed token from
        the cache automatically.

        :param endpoint: The endpoint to call.
        :type endpoint: HTTPEndpoint
        :returns: The handled HTTP response.
        :rtype: HTTPResponse
        """
        token_before = self.sinch.configuration.token_manager.token
        http_response = self.send(endpoint)

        if self._should_refresh_token(endpoint, http_response):
            used_token = token_before.access_token if token_before else None
            self.sinch.configuration.token_manager.refresh_auth_token(used_token)
            http_response = self.send(endpoint)

        return endpoint.handle_response(http_response)

    @staticmethod
    def _should_refresh_token(endpoint: HTTPEndpoint, http_response: HTTPResponse) -> bool:
        """
        Returns True for an OAuth endpoint that got a 401 with an expired-token header.

        :param endpoint: The endpoint that was called.
        :type endpoint: HTTPEndpoint
        :param http_response: The response received.
        :type http_response: HTTPResponse
        :returns: Whether the token should be refreshed and the request retried.
        :rtype: bool
        """
        if endpoint.HTTP_AUTHENTICATION != HTTPAuthentication.OAUTH.value:
            return False
        if http_response.status_code != 401:
            return False
        www_authenticate = http_response.headers.get("www-authenticate") or ""
        return "expired" in www_authenticate

    @staticmethod
    def _get_bearer_token_from_request(request_data: HttpRequest) -> Optional[str]:
        """
        Extracts the bearer token from the request's Authorization header.

        :param request_data: The request.
        :type request_data: HttpRequest
        :returns: The bearer token, or None if absent or not a bearer.
        :rtype: Optional[str]
        """
        auth = request_data.headers.get("Authorization", "")
        return auth.removeprefix("Bearer ") if auth.startswith("Bearer ") else None

    @staticmethod
    def _set_bearer_token(request_data: HttpRequest, token: str) -> None:
        """
        Stamps the bearer token onto the request's Authorization header.

        :param request_data: The request.
        :type request_data: HttpRequest
        :param token: The bearer token.
        :type token: str
        """
        request_data.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
