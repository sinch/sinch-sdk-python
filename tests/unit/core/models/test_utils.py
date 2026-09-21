"""Tests for sinch.core.models.utils helpers."""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from sinch.core.models.utils import (
    model_dump_for_query_params,
    serialize_datetime_in_dict,
)


class TestModelDumpForQueryParams:
    def test_simple_fields_returned_as_is(self):
        class M(BaseModel):
            batch_id: str
            status: Optional[str] = None

        result = model_dump_for_query_params(
            M(batch_id="01FC66621XXXXX119Z8PMV1QPQ", status="delivered")
        )
        assert result["batch_id"] == "01FC66621XXXXX119Z8PMV1QPQ"
        assert result["status"] == "delivered"

    def test_lists_converted_to_comma_separated_strings(self):
        class M(BaseModel):
            status: Optional[List[str]] = None
            code: Optional[List[int]] = None

        result = model_dump_for_query_params(
            M(status=["Delivered", "Failed"], code=[15, 0])
        )
        assert result["status"] == "Delivered,Failed"
        assert result["code"] == "15,0"

    def test_empty_values_filtered_out(self):
        class M(BaseModel):
            batch_id: str
            status: str = ""
            code: List[int] = []

        result = model_dump_for_query_params(
            M(batch_id="01FC66621XXXXX119Z8PMV1QPQ", status="", code=[])
        )
        assert result["batch_id"] == "01FC66621XXXXX119Z8PMV1QPQ"
        assert "status" not in result
        assert "code" not in result

    def test_none_values_excluded_by_default(self):
        class M(BaseModel):
            batch_id: str
            status: Optional[str] = None

        result = model_dump_for_query_params(M(batch_id="abc"))
        assert result == {"batch_id": "abc"}

    def test_none_values_kept_when_exclude_none_false(self):
        class M(BaseModel):
            batch_id: str
            status: Optional[str] = None

        result = model_dump_for_query_params(M(batch_id="abc"), exclude_none=False)
        assert result["status"] is None

    def test_by_alias_toggles_field_alias(self):
        from pydantic import Field

        class WithAlias(BaseModel):
            page_size: int = Field(default=10, alias="pageSize")

            model_config = {"populate_by_name": True}

        result = model_dump_for_query_params(WithAlias())
        assert result["pageSize"] == 10

        result_no_alias = model_dump_for_query_params(WithAlias(), by_alias=False)
        assert result_no_alias["page_size"] == 10

    def test_exclude_omits_fields(self):
        class M(BaseModel):
            batch_id: str
            status: str

        result = model_dump_for_query_params(
            M(batch_id="abc", status="delivered"), exclude={"batch_id"}
        )
        assert "batch_id" not in result
        assert result["status"] == "delivered"

    def test_single_item_list_converted_to_string(self):
        class M(BaseModel):
            status: List[str] = []

        result = model_dump_for_query_params(M(status=["Delivered"]))
        assert result["status"] == "Delivered"


class TestSerializeDatetimeInDict:
    def test_none_returns_none(self):
        assert serialize_datetime_in_dict(None) is None

    def test_empty_dict_returns_empty_dict(self):
        assert serialize_datetime_in_dict({}) == {}

    def test_datetime_converted_to_iso_date_dropping_time(self):
        # datetime is intentionally truncated to date: time component is discarded.
        result = serialize_datetime_in_dict(
            {"start": datetime(2026, 7, 2, 15, 30, 45)}
        )
        assert result == {"start": "2026-07-02"}

    def test_date_converted_to_iso_date(self):
        result = serialize_datetime_in_dict({"start": date(2026, 7, 2)})
        assert result == {"start": "2026-07-02"}

    def test_string_values_passed_through_unchanged(self):
        result = serialize_datetime_in_dict({"start": "2026-07-02", "name": "batch"})
        assert result == {"start": "2026-07-02", "name": "batch"}

    def test_non_datetime_values_passed_through_unchanged(self):
        value = {"count": 5, "active": True, "tags": ["a", "b"], "meta": None}
        assert serialize_datetime_in_dict(value) == value

    def test_mixed_values(self):
        result = serialize_datetime_in_dict(
            {
                "created": datetime(2026, 1, 1, 12, 0, 0),
                "expires": date(2026, 12, 31),
                "label": "promo",
                "limit": 100,
            }
        )
        assert result == {
            "created": "2026-01-01",
            "expires": "2026-12-31",
            "label": "promo",
            "limit": 100,
        }

    def test_original_dict_not_mutated(self):
        original = {"start": datetime(2026, 7, 2, 15, 30, 45)}
        serialize_datetime_in_dict(original)
        assert isinstance(original["start"], datetime)
