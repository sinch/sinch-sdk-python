from typing import TypedDict, Union


class CoordinatesDict(TypedDict):
    latitude: Union[int, float]
    longitude: Union[int, float]
