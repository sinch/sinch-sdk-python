from typing import Annotated, Union
from pydantic import Field
from sinch.domains.sms.models.v1.shared.mo_text_message import MOTextMessage
from sinch.domains.sms.models.v1.shared.mo_binary_message import MOBinaryMessage
from sinch.domains.sms.models.v1.shared.mo_media_message import MOMediaMessage

_InboundMessageUnion = Union[MOTextMessage, MOBinaryMessage, MOMediaMessage]

InboundMessage = Annotated[_InboundMessageUnion, Field(discriminator="type")]
