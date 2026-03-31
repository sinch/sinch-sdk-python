from typing import Literal, Union
from pydantic import StrictStr

WhatsAppInteractiveNfmReplyNameType = Union[
    Literal["flow", "address_message"],
    StrictStr,
]
