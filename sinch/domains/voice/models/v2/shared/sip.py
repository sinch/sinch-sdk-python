from typing import Literal, Optional, Union

from pydantic import Field, StrictStr, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.shared.call_header import CallHeader


class SipDetails(BaseModelConfiguration):
    endpoint: StrictStr = Field(
        default=...,
        description="SIP URI of the destination endpoint. Both `sip:` (unencrypted) and `sips:` (TLS-encrypted) schemes are supported. Must be at most 256 characters, matching the pattern `^sips?:`.",
    )
    transport: Optional[Union[Literal["UDP", "TCP", "TLS"], StrictStr]] = (
        Field(
            default=None,
            description="Transport protocol to use for the SIP signalling channel.\n\nIf omitted, the platform selects a default based on the URI scheme: `UDP` for `sip:` and `TLS` for `sips:`. Setting this explicitly overrides that default - for example, to force `TCP` for a `sip:` URI or to use `TLS` without switching to the `sips:` scheme.",
        )
    )
    call_headers: Optional[conlist(CallHeader)] = Field(
        default=None,
        alias="callHeaders",
        description="Custom SIP headers to be sent in the call setup.",
    )


class Sip(BaseModelConfiguration):
    type: Literal["SIP"] = Field(
        default="SIP",
        description="Routes the call to a SIP (Session Initiation Protocol) endpoint.",
    )
    sip: SipDetails = Field(default=...)
