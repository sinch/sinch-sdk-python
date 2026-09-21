from typing import Literal, Optional, Union

from pydantic import Field, StrictStr
from typing_extensions import Annotated

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class Say(BaseModelConfiguration):
    text: StrictStr = Field(
        default=...,
        description="The text to be synthesized into speech.\n\nIf `format` is `TEXT` (default), provide plain text.\nIf `format` is `SSML`, provide a valid SSML document (for example, `<speak>...</speak>`).",
    )
    format: Optional[Union[Literal["TEXT", "SSML"], StrictStr]] = Field(
        default=None, description="Format of the message"
    )
    voice_name: StrictStr = Field(
        default=...,
        alias="voiceName",
        description="The name of the voice to use for text-to-speech synthesis.\n\nSupported voices include: Emma, Brian, and others. For a complete list of available voices and their characteristics, see the [Text-to-Speech Voices documentation](/docs/voice/api-reference/text-to-speech-voices).",
    )


class SayMessage(BaseModelConfiguration):
    type: Literal["SAY"] = Field(
        default="SAY",
        description="Text-to-speech message to be played during the call.",
    )
    say: Say = Field(default=...)


class Play(BaseModelConfiguration):
    url: StrictStr = Field(default=..., description="URL of the media to send")


class PlayMessage(BaseModelConfiguration):
    type: Literal["PLAY"] = Field(
        default="PLAY", description="Audio file playback during the call."
    )
    play: Play = Field(default=...)


Message = Annotated[
    Union[SayMessage, PlayMessage], Field(discriminator="type")
]
