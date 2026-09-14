from typing import Literal, Union

from pydantic import StrictStr

RecordingDestinationType = Union[Literal["AWS", "GCP", "AZURE"], StrictStr]
