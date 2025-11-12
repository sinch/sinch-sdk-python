from typing import Annotated, Union
from pydantic import Field
from sinch.domains.sms.models.v1.shared.text_response import TextResponse
from sinch.domains.sms.models.v1.shared.binary_response import BinaryResponse
from sinch.domains.sms.models.v1.shared.media_response import MediaResponse

# Union type for isinstance checks
_BatchResponseUnion = Union[TextResponse, BinaryResponse, MediaResponse]

# Discriminated union for validation
BatchResponse = Annotated[_BatchResponseUnion, Field(discriminator="type")]
