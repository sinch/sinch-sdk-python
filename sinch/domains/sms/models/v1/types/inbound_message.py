from sinch.core.models.internal.unions import ResolveUnion
from typing import Annotated, Union
from sinch.domains.sms.models.v1.shared.mo_text_message import MOTextMessage
from sinch.domains.sms.models.v1.shared.mo_binary_message import (
    MOBinaryMessage,
)
from sinch.domains.sms.models.v1.shared.mo_media_message import MOMediaMessage

InboundMessage = Annotated[
    Union[
        MOTextMessage,
        MOBinaryMessage,
        MOMediaMessage,
    ],
    ResolveUnion(discriminator="type"),
]
