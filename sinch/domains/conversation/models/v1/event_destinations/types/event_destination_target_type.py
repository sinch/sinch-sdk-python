from typing import Literal, Union

from pydantic import StrictStr


EventDestinationTargetType = Union[Literal["DISMISS", "HTTP"], StrictStr]
