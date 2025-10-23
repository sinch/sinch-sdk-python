from typing import Literal, Union
from pydantic import StrictStr


DeliveryReportType = Union[Literal["summary", "full"], StrictStr]
