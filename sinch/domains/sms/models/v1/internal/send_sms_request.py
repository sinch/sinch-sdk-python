from typing import Union
from sinch.domains.sms.models.v1.shared.text_request import TextRequest
from sinch.domains.sms.models.v1.shared.binary_request import (
    BinaryRequest,
)
from sinch.domains.sms.models.v1.shared.media_request import (
    MediaRequest,
)


SendSMSRequest = Union[
    TextRequest,
    BinaryRequest,
    MediaRequest,
]
