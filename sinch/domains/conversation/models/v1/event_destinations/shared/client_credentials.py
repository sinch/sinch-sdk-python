from typing import Literal, Optional, Union

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ClientCredentials(BaseModelConfiguration):
    client_id: StrictStr = Field(
        default=...,
        description="The Client ID that will be used in the OAuth2 Client Credentials flow.",
    )
    client_secret: StrictStr = Field(
        default=...,
        description="The Client Secret that will be used in the OAuth2 Client Credentials flow.",
    )
    endpoint: StrictStr = Field(
        default=...,
        description="The endpoint that will be used in the OAuth2 Client Credentials flow. Expected to return a JSON with an access token and `expires_in` value (in seconds). The `expires_in` value, which must be a minimum of 30 seconds and a maximum of 3600 seconds, is how long Sinch will save the access token before asking for a new one.",
    )
    scope: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Space-separated string per RFC 6749. Used to limit the access granted by the token. Max length: 1024 characters. If blank or omitted, this is not included in the token request. Max length: 1024 characters.",
    )
    response_type: Optional[StrictStr] = Field(
        default=None,
        description="Optional. When granting `client_credentials`, this is generally omitted. If you do provide a value, it will be forwarded to your OAuth provider as-is. Max length: 64 characters.",
    )
    token_request_type: Optional[
        Union[Literal["BASIC", "FORM"], StrictStr]
    ] = Field(
        default=None,
        description="Optional. Controls how `client_id` and `client_secret` are sent to the token endpoint. Either `BASIC` or `FORM`. If not set or unrecognized, `BASIC` is used by default. `BASIC`: Sent using the HTTP Authorization header (Basic auth). In this case, `client_id` and `client_secret` are NOT included in the form body. `FORM`: Sent in the form body as `client_id` and `client_secret`. No Authorization header is added.",
    )
