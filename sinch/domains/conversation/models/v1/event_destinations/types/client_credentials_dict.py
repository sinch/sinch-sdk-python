from typing import Literal, TypedDict, Union

from typing_extensions import NotRequired


class ClientCredentialsDict(TypedDict):
    client_id: str
    """The Client ID that will be used in the OAuth2 Client Credentials flow."""

    client_secret: str
    """The Client Secret that will be used in the OAuth2 Client Credentials flow."""

    endpoint: str
    """The endpoint that will be used in the OAuth2 Client Credentials flow. Expected to return a JSON with an access token and `expires_in` value (in seconds). The `expires_in` value, which must be a minimum of 30 seconds and a maximum of 3600 seconds, is how long Sinch will save the access token before asking for a new one."""

    scope: NotRequired[str]
    """Optional. Space-separated string per RFC 6749. Used to limit the access granted by the token. Max length: 1024 characters. If blank or omitted, this is not included in the token request. Max length: 1024 characters."""

    response_type: NotRequired[str]
    """Optional. When granting `client_credentials`, this is generally omitted. If you do provide a value, it will be forwarded to your OAuth provider as-is. Max length: 64 characters."""

    token_request_type: NotRequired[Union[Literal["BASIC", "FORM"], str]]
    """Optional. Controls how `client_id` and `client_secret` are sent to the token endpoint. Either `BASIC` or `FORM`. If not set or unrecognized, `BASIC` is used by default. `BASIC`: Sent using the HTTP Authorization header (Basic auth). In this case, `client_id` and `client_secret` are NOT included in the form body. `FORM`: Sent in the form body as `client_id` and `client_secret`. No Authorization header is added."""
