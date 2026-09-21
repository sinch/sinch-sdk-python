from typing import Literal, Union
from pydantic import StrictStr


DispatchRetentionPolicyType = Union[
    Literal["MESSAGE_EXPIRE_POLICY"], StrictStr
]
