from typing import Literal, Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class SipFromDetails(BaseModelConfiguration):
    endpoint: StrictStr = Field(
        default=...,
        description="SIP URI of the originating endpoint. Both `sip:` (unencrypted) and `sips:` (TLS-encrypted) schemes are supported.",
    )
    display_name: Optional[StrictStr] = Field(
        default=None,
        alias="displayName",
        description="Display name presented to the called party as the caller identity. Transmitted as the display name part of the SIP `From` header (for example, `Alice <sip:alice@example.com>`).",
    )


class SipFrom(BaseModelConfiguration):
    type: Literal["SIP"] = Field(
        default="SIP",
        description="Indicates the call originated from a SIP (Session Initiation Protocol) endpoint.",
    )
    sip: SipFromDetails = Field(default=...)
