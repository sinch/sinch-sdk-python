from pydantic import conlist, StrictStr
from typing import Literal, Union

NumberTypesRegionsValuesList = conlist(
    Union[Literal["MOBILE", "LOCAL", "TOLL_FREE", "NUMBER_TYPE_UNSPECIFIED"], StrictStr], min_length=1
)
