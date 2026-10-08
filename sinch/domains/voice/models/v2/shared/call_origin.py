from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion


from sinch.domains.voice.models.v2.shared.phone import Phone
from sinch.domains.voice.models.v2.shared.sip_from import SipFrom

CallOrigin = Annotated[
    Union[
        Phone,
        SipFrom,
    ],
    ResolveUnion(discriminator="type"),
]
