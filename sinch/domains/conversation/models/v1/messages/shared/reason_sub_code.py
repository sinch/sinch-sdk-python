from typing import Literal, Union
from pydantic import StrictStr


ReasonSubCode = Union[
    Literal[
        "UNSPECIFIED_SUB_CODE",
        "ATTACHMENT_REJECTED",
        "MEDIA_TYPE_UNDETERMINED",
        "INACTIVE_SENDER",
    ],
    StrictStr,
]
