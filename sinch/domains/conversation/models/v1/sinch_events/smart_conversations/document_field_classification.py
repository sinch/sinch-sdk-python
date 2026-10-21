from typing import Dict, Optional

from pydantic import Field, conlist

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.document_field_data import (
    DocumentFieldData,
)


class DocumentFieldClassification(SinchEvent):
    """An object containing a result object that reports on all identified fields, as well as the values assigned to those fields."""

    result: Optional[conlist(Dict[str, DocumentFieldData])] = Field(
        default=None,
        description="The result of the Document Field Classification process",
    )
