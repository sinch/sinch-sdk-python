from typing import Literal, Union
from pydantic import StrictStr


RetentionPolicyType = Union[
    Literal[
        "MESSAGE_EXPIRE_POLICY",
        "CONVERSATION_EXPIRE_POLICY",
        "PERSIST_RETENTION_POLICY",
    ],
    StrictStr,
]
