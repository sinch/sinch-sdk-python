from typing import Literal, Union
from pydantic import StrictStr


OrderBy = Union[Literal["PHONE_NUMBER", "DISPLAY_NAME"], StrictStr]
