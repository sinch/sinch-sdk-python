from sinch.core.models.internal.unions import ResolveUnion
from typing import Annotated, Union
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_text_header import (
    WhatsAppInteractiveTextHeader,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_image_header import (
    WhatsAppInteractiveImageHeader,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_document_header import (
    WhatsAppInteractiveDocumentHeader,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_video_header import (
    WhatsAppInteractiveVideoHeader,
)

WhatsAppInteractiveHeader = Annotated[
    Union[
        WhatsAppInteractiveTextHeader,
        WhatsAppInteractiveImageHeader,
        WhatsAppInteractiveDocumentHeader,
        WhatsAppInteractiveVideoHeader,
    ],
    ResolveUnion(discriminator="type"),
]
