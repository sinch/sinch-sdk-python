from typing import List, Literal, TypedDict, Union

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.list_message_dict import (
    ProductItemDict,
)
from sinch.domains.conversation.models.v1.messages.types.location_message_dict import (
    LocationMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.media_properties_dict import (
    MediaPropertiesDict,
)
from sinch.domains.conversation.models.v1.messages.types.reason_code_type import (
    ReasonCodeType,
)
from sinch.domains.conversation.models.v1.messages.types.reason_sub_code_type import (
    ReasonSubCodeType,
)
from sinch.domains.conversation.models.v1.messages.types.text_message_dict import (
    TextMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.whatsapp_interactive_nfm_reply_name_type import (
    WhatsAppInteractiveNfmReplyNameType,
)


class WhatsAppInteractiveNfmReplyDict(TypedDict):
    name: WhatsAppInteractiveNfmReplyNameType
    response_json: str
    body: str


class WhatsAppInteractiveNfmReplyMessageDict(TypedDict):
    type: Union[Literal["nfm_reply"], str]
    nfm_reply: WhatsAppInteractiveNfmReplyDict


class ChannelSpecificContactMessageDict(TypedDict):
    message_type: Union[Literal["nfm_reply"], str]
    message: WhatsAppInteractiveNfmReplyMessageDict


class ChoiceResponseMessageDict(TypedDict):
    message_id: str
    postback_data: str


class ReasonDict(TypedDict):
    code: NotRequired[ReasonCodeType]
    description: NotRequired[str]
    sub_code: NotRequired[ReasonSubCodeType]
    channel_code: NotRequired[str]


class FallbackMessageDict(TypedDict):
    raw_message: NotRequired[str]
    reason: NotRequired[ReasonDict]


class MediaCardMessageDict(TypedDict):
    url: str
    caption: NotRequired[str]


class ProductResponseMessageDict(TypedDict):
    products: NotRequired[List[ProductItemDict]]
    title: NotRequired[str]
    catalog_id: NotRequired[str]


class ReplyToDict(TypedDict):
    message_id: str


class ContactMessageDict(TypedDict):
    channel_specific_message: NotRequired[ChannelSpecificContactMessageDict]
    choice_response_message: NotRequired[ChoiceResponseMessageDict]
    fallback_message: NotRequired[FallbackMessageDict]
    location_message: NotRequired[LocationMessageDict]
    media_card_message: NotRequired[MediaCardMessageDict]
    media_message: NotRequired[MediaPropertiesDict]
    product_response_message: NotRequired[ProductResponseMessageDict]
    text_message: NotRequired[TextMessageDict]
    reply_to: NotRequired[ReplyToDict]
