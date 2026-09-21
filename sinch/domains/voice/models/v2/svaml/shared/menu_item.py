from typing import Dict, Literal, Optional, Union

from pydantic import Field, StrictInt, StrictStr, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.menu_prompt import MenuPrompt


class MenuItem(BaseModelConfiguration):
    prompt: Optional[MenuPrompt] = Field(
        default=None,
        description="Prompt played when this menu starts.\n\nThis prompt is also used as the repeat prompt when repeatPrompt is not defined for the menu.",
    )
    repeat_prompt: Optional[MenuPrompt] = Field(
        default=None,
        alias="repeatPrompt",
        description="Prompt played when the menu is repeated.\n\nRepeats occur when input times out or when the provided input does not match any menu match item.",
    )
    input_timeout_duration_seconds: Optional[StrictInt] = Field(
        default=None,
        alias="inputTimeoutDurationSeconds",
        description="Maximum number of seconds to wait for user input before the input attempt times out. Must be between 1 and 60 seconds; defaults to 5 if not set.",
    )
    repeat_count: Optional[StrictInt] = Field(
        default=None,
        alias="repeatCount",
        description="Maximum number of times the menu is repeated.\n\nA repeat occurs when input times out or when the provided input does not match any menu match item.",
    )
    minimum_input_length: Optional[StrictInt] = Field(
        default=None,
        alias="minimumInputLength",
        description="Minimum number of input characters required before the menu evaluates the collected input.",
    )
    maximum_input_length: Optional[StrictInt] = Field(
        default=None,
        alias="maximumInputLength",
        description="Maximum number of input characters that triggers the menu to evaluate the collected input.",
    )
    terminating_sequence: Optional[StrictStr] = Field(
        default=None,
        alias="terminatingSequence",
        description="Character sequence that signals the end of input and triggers immediate evaluation.\n\nUseful when variable-length input is allowed and shorter valid options should be submitted without waiting for timeout or maximum length.\n\nThe terminating sequence value is included in the evaluated input.",
    )
    input_methods: Optional[conlist(Union[Literal["DTMF"], StrictStr])] = (
        Field(
            default=None,
            alias="inputMethods",
            description="Input methods accepted for this menu when collecting user input.",
        )
    )
    matches: Optional[Dict[StrictStr, conlist("SvamlCommand")]] = Field(
        default=None,
        description="Items matched against the collected input. Maximum number of allowed match expressions is 50.\n\nDefined as a dictionary where each property name is a literal or a regular expression string.\n\nValues are evaluated in the order they are defined.",
    )
    on_fail: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onFail",
        description="SVAML commands executed when the menu fails to collect a matching input.\n\nThis handler runs after the repeat limit is reached without any input matching a menu match item.",
    )
