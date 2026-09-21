from typing import List, TypedDict

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.svaml.types.message_dict import MessageDict


class MenuPromptDict(TypedDict):
    messages: List[MessageDict]
    allow_barge_in: NotRequired[bool]
