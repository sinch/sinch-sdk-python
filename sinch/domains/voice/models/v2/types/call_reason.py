from typing import Literal, Union

from pydantic import StrictStr

CallReason = Union[
    Literal[
        "OK",
        "NOT_AVAILABLE",
        "CALLER_HANGUP",
        "CALLEE_HANGUP",
        "MANAGER_HANGUP",
        "DID_NOT_FOUND",
        "INVALID_SCRIPT",
        "UNKNOWN_PRODUCT",
        "NO_MORE_ROUTES",
        "ERROR",
    ],
    StrictStr,
]
