from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.sms.models.v1.shared.text_request import TextRequest
from sinch.domains.sms.models.v1.shared.binary_request import (
    BinaryRequest,
)
from sinch.domains.sms.models.v1.shared.media_request import (
    MediaRequest,
)


SendSMSRequest = Annotated[
    Union[
        TextRequest,
        BinaryRequest,
        MediaRequest,
    ],
    ResolveUnion(discriminator="type", discriminator_strict=False),
]
