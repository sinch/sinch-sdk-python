from typing import Optional
from pydantic import Field, StrictBool
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ContactSettings(BaseModelConfiguration):
    unified_contact_id_enabled: Optional[StrictBool] = Field(
        default=None,
        description="Enables the Unified Contact ID feature. When enabled, contacts with the same phone number across SMS, RCS, and MMS channels are treated as a single entity. [See the documentation](https://developers.sinch.com/docs/conversation/unified-contact-id/) for details and requirements.",
    )
