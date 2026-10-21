from typing import Literal, Union

from pydantic import StrictStr

ReactionActionType = Union[
    Literal[
        "REACTION_ACTION_UNKNOWN",
        "REACTION_ACTION_REACT",
        "REACTION_ACTION_UNREACT",
    ],
    StrictStr,
]
