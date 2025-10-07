from typing import Literal, Union
from pydantic import StrictStr


OrderByType = Union[Literal["PHONE_NUMBER", "DISPLAY_NAME"], StrictStr]
