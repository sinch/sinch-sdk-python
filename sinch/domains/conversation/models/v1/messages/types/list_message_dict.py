from typing import List, TypedDict, Union
from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.media_properties_dict import (
    MediaPropertiesDict,
)


class ChoiceItemDict(TypedDict):
    title: str
    description: NotRequired[str]
    media: NotRequired[MediaPropertiesDict]
    postback_data: NotRequired[str]


class ProductItemDict(TypedDict):
    id: str
    marketplace: str
    quantity: NotRequired[int]
    item_price: NotRequired[Union[int, float]]
    currency: NotRequired[str]


class ListItemChoiceDict(TypedDict):
    choice: ChoiceItemDict


class ListItemProductDict(TypedDict):
    product: ProductItemDict


ListItemDict = Union[ListItemChoiceDict, ListItemProductDict]


class ListSectionDict(TypedDict):
    items: List[ListItemDict]
    title: NotRequired[str]


class ListMessagePropertiesDict(TypedDict):
    catalog_id: NotRequired[str]
    menu: NotRequired[str]
    whatsapp_header: NotRequired[str]


class ListMessageDict(TypedDict):
    title: str
    sections: List[ListSectionDict]
    description: NotRequired[str]
    media: NotRequired[MediaPropertiesDict]
    message_properties: NotRequired[ListMessagePropertiesDict]
