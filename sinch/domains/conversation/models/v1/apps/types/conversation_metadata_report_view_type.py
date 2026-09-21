from typing import Literal, Union
from pydantic import StrictStr


ConversationMetadataReportViewType = Union[Literal["NONE", "FULL"], StrictStr]
