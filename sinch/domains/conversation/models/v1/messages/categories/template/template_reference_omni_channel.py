from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.categories.template import (
    TemplateReferenceChannelSpecific,
)


class TemplateReferenceOmniChannel(TemplateReferenceChannelSpecific):
    version: StrictStr = Field(
        ...,
        description="Used to specify what version of a template to use. Required when using `omni_channel_override` and `omni_template` fields. This will be used in conjunction with `language_code`. Note that, when referencing omni-channel templates using the [Sinch Customer Dashboard](https://dashboard.sinch.com/), the latest version of a given omni-template can be identified by populating this field with `latest`.",
    )
