from datetime import datetime
from typing import Dict, Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.templates.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.templates.models.v2.shared.channel_template_override import (
    ChannelTemplateOverride,
)
from sinch.domains.conversation.templates.models.v2.shared.template_variable import (
    TemplateVariable,
)


class TemplateTranslationBase(BaseModelConfiguration):
    language_code: StrictStr = Field(
        default=...,
        description="The BCP-47 language code, such as `en-US` or `sr-Latn`. For more information, see https://www.unicode.org/reports/tr35/#Unicode_locale_identifier.",
    )
    version: Optional[StrictStr] = Field(
        default=None, description="The version of the translation."
    )
    channel_template_overrides: Optional[
        Dict[ConversationChannelType, ChannelTemplateOverride]
    ] = Field(
        default=None,
        description="Field to override the omnichannel template by referring to a channel-specific template. The key in the map must point to a valid conversation channel. Currently only `WHATSAPP` and `KAKAOTALK` are supported",
    )
    variables: Optional[conlist(TemplateVariable)] = Field(
        default=None,
        description="List of expected variables. Can be used for request validation.",
    )
    create_time: Optional[datetime] = Field(
        default=None, description="Timestamp when the translation was created."
    )
    update_time: Optional[datetime] = Field(
        default=None,
        description="Timestamp of when the translation was updated.",
    )
