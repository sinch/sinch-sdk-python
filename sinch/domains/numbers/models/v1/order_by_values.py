from typing import Literal, Union
from pydantic import StrictStr

OrderByValues = Union[Literal["PHONE_NUMBER", "DISPLAY_NAME"], StrictStr]
