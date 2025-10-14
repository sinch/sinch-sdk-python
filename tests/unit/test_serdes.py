import json
import datetime
from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel, SinchRequestBaseModel
from sinch.core.deserializers import timestamp_to_datetime_in_utc_deserializer


@dataclass
class SampleDataModel(SinchBaseModel):
    writing: str
    unit: str
    tests: str
    is_: str
    boring: str


@dataclass
class SampleRequestDataModel(SinchRequestBaseModel):
    request_time_off: bool
    quantity: int
    accepted: bool = None


def construct_test_data_model():
    return SampleDataModel(writing="meh", unit="necessary", tests="...really!", is_="Today?Monday!", boring="no_way...")


def construct_request_test_data_model():
    return SampleRequestDataModel(request_time_off=True, quantity=20)


def test_sinch_base_model_serialization_to_json():
    test_model = construct_test_data_model()
    test_model_json = test_model.as_json()
    assert "necessary" in test_model_json

    test_model_dict = json.loads(test_model_json)
    assert isinstance(test_model_dict, dict)


def test_sinch_base_model_transformation_to_python_dict():
    test_model = construct_test_data_model()
    test_model_json = test_model.as_dict()
    assert test_model_json.get("boring")


def test_sinch_request_base_model_empty_field_removal():
    test_data_model = construct_request_test_data_model()
    request_data_model_as_dict = test_data_model.as_dict()
    assert not request_data_model_as_dict.get("accepted")


def test_timestamp_to_datetime_in_utc_deserializer():
    datetime_in_utc = timestamp_to_datetime_in_utc_deserializer("2024-02-15T13:01:29")
    assert isinstance(datetime_in_utc, datetime.datetime)
    assert datetime_in_utc.tzinfo == datetime.timezone.utc


def test_timestamp_to_datetime_in_utc_deserializer_with_added_tz():
    datetime_in_utc = timestamp_to_datetime_in_utc_deserializer("2024-02-15T13:01:29Z")
    assert isinstance(datetime_in_utc, datetime.datetime)
    assert datetime_in_utc.tzinfo == datetime.timezone.utc
