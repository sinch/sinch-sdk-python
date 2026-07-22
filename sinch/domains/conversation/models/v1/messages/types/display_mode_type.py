from typing import Literal, Union

from pydantic import StrictStr

DisplayModeType = Union[
    Literal["DISPLAY_MODE_UNSPECIFIED", "PERSISTENT"],
    StrictStr,
]
