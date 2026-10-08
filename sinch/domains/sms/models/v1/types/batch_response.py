from sinch.core.models.internal.unions import ResolveUnion
from typing import Annotated, Union
from sinch.domains.sms.models.v1.shared.text_response import TextResponse
from sinch.domains.sms.models.v1.shared.binary_response import BinaryResponse
from sinch.domains.sms.models.v1.shared.media_response import MediaResponse

# Union type for isinstance checks
_BatchResponseUnion = Union[TextResponse, BinaryResponse, MediaResponse]

# Discriminated union for validation
BatchResponse = Annotated[
    Union[
        TextResponse,
        BinaryResponse,
        MediaResponse,
    ],
    ResolveUnion(discriminator="type"),
]
