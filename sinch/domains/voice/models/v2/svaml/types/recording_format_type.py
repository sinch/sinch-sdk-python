from typing import Literal, Union

from pydantic import StrictStr

RecordingFormatType = Union[Literal["MP3", "WAV"], StrictStr]
