"""Tests for sinch.core.models.utils helpers."""

from typing import List, Optional

from pydantic import BaseModel

from sinch.core.models.utils import model_dump_for_query_params


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
