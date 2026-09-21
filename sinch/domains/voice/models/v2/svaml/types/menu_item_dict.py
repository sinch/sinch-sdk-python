from typing import TYPE_CHECKING, Dict, List, Literal, TypedDict, Union

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.svaml.types.menu_prompt_dict import (
    MenuPromptDict,
)

if TYPE_CHECKING:
    from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
        SvamlCommandDict,
    )


class MenuItemDict(TypedDict):
    prompt: NotRequired[MenuPromptDict]
    repeat_prompt: NotRequired[MenuPromptDict]
    input_timeout_duration_seconds: NotRequired[int]
    repeat_count: NotRequired[int]
    minimum_input_length: NotRequired[int]
    maximum_input_length: NotRequired[int]
    terminating_sequence: NotRequired[str]
    input_methods: NotRequired[List[Union[Literal["DTMF"], str]]]
    matches: NotRequired[Dict[str, List["SvamlCommandDict"]]]
    on_fail: NotRequired[List["SvamlCommandDict"]]
