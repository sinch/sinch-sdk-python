from datetime import datetime
from typing import TypedDict, Union
from typing_extensions import NotRequired


class RndFeatureOptionsDict(TypedDict):
    contact_date: NotRequired[Union[str, datetime]]
