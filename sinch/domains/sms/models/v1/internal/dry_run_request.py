from sinch.core.models.internal.unions import ResolveUnion
from typing import Annotated, Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictInt
from sinch.domains.sms.models.v1.shared.text_request import TextRequest
from sinch.domains.sms.models.v1.shared.binary_request import (
    BinaryRequest,
)
from sinch.domains.sms.models.v1.shared.media_request import (
    MediaRequest,
)


class DryRunMixin(BaseModel):
    """Mixin that adds dry run query parameters to request models."""

    per_recipient: Optional[StrictBool] = Field(
        default=None,
        description="Whether to include per recipient details in the response",
    )
    number_of_recipients: Optional[StrictInt] = Field(
        default=None,
        description="Max number of recipients to include per recipient details for in the response",
    )


class DryRunTextRequest(DryRunMixin, TextRequest):
    """Request model for dry run with a text message."""

    pass


class DryRunBinaryRequest(DryRunMixin, BinaryRequest):
    """Request model for dry run with a binary message."""

    pass


class DryRunMediaRequest(DryRunMixin, MediaRequest):
    """Request model for dry run with a media message."""

    pass


DryRunRequest = Annotated[
    Union[
        DryRunTextRequest,
        DryRunBinaryRequest,
        DryRunMediaRequest,
    ],
    ResolveUnion(discriminator="type", discriminator_strict=False),
]
