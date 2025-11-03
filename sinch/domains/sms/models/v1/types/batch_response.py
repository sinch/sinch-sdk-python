from typing import Union
from sinch.domains.sms.models.v1.shared.text_response import TextResponse
from sinch.domains.sms.models.v1.shared.binary_response import BinaryResponse
from sinch.domains.sms.models.v1.shared.media_response import MediaResponse


BatchResponse = Union[TextResponse, BinaryResponse, MediaResponse]
