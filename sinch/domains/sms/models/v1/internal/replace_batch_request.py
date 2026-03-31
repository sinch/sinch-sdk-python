from typing import Union
from sinch.domains.sms.models.v1.shared.text_request import TextRequest
from sinch.domains.sms.models.v1.shared.binary_request import (
    BinaryRequest,
)
from sinch.domains.sms.models.v1.shared.media_request import (
    MediaRequest,
)
from sinch.domains.sms.models.v1.shared.batch_id_mixin import BatchIdMixin


class ReplaceTextRequest(BatchIdMixin, TextRequest):
    """Request model for replacing a batch with a text message."""

    pass


class ReplaceBinaryRequest(BatchIdMixin, BinaryRequest):
    """Request model for replacing a batch with a binary message."""

    pass


class ReplaceMediaRequest(BatchIdMixin, MediaRequest):
    """Request model for replacing a batch with a media message."""

    pass


ReplaceBatchRequest = Union[
    ReplaceTextRequest,
    ReplaceBinaryRequest,
    ReplaceMediaRequest,
]
