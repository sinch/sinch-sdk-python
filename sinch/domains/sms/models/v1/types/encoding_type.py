from typing import Literal, Union
from pydantic import StrictStr


EncodingType = Union[Literal["GSM", "UNICODE"], StrictStr]
