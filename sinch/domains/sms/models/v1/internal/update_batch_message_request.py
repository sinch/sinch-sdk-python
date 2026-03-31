from typing import Union
from sinch.domains.sms.models.v1.internal.update_text_request import (
    UpdateTextRequest,
)
from sinch.domains.sms.models.v1.internal.update_binary_request import (
    UpdateBinaryRequest,
)
from sinch.domains.sms.models.v1.internal.update_media_request import (
    UpdateMediaRequest,
)
from sinch.domains.sms.models.v1.shared.batch_id_mixin import BatchIdMixin


class UpdateTextRequestWithBatchId(BatchIdMixin, UpdateTextRequest):
    """Request model for updating a batch with a text message."""

    pass


class UpdateBinaryRequestWithBatchId(BatchIdMixin, UpdateBinaryRequest):
    """Request model for updating a batch with a binary message."""

    pass


class UpdateMediaRequestWithBatchId(BatchIdMixin, UpdateMediaRequest):
    """Request model for updating a batch with a media message."""

    pass


UpdateBatchMessageRequest = Union[
    UpdateTextRequestWithBatchId,
    UpdateBinaryRequestWithBatchId,
    UpdateMediaRequestWithBatchId,
]
