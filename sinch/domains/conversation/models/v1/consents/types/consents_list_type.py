from typing import Literal, Union

from pydantic import StrictStr


ConsentsListType = Union[
    Literal["OPT_OUT_ALL", "OPT_OUT_MARKETING", "OPT_OUT_NOTIFICATION"],
    StrictStr,
]
