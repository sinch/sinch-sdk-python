"""Tests for the core base model configuration.

Covers the module-level case helpers, the private mixins and the three
public model classes (BaseConfigModel, SnakeCaseExtrasModel,
CamelCaseDumpModel) including composition behavior.
"""

import json
from typing import Any, Dict, Optional

import pytest
from pydantic import Field

from sinch.core.models.internal.base_model_config import (
    BaseConfigModel,
    CamelCaseDumpModel,
    SnakeCaseExtrasModel,
    _camelize_keys,
    _to_camel_case,
    _to_snake_case,
    transform_kwargs_casing_scope,
)


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------


class TestToCamelCase:
    @pytest.mark.parametrize(
        "snake, camel",
        [
            ("foo_bar", "fooBar"),
            ("hello_world", "helloWorld"),
            ("this_is_a_test", "thisIsATest"),
            ("PHONE_NUMBER", "phoneNumber"),
            ("appId", "appId"),
        ],
    )
    def test_standard_cases(self, snake, camel):
        assert _to_camel_case(snake) == camel

    @pytest.mark.parametrize(
        "snake, camel",
        [
            # Documented deviation from pydantic.alias_generators.to_camel:
            # consecutive underscores are preserved rather than collapsed.
            ("foo__bar", "foo_Bar"),
            ("foo___bar", "foo__Bar"),
            ("trailing_", "trailing_"),
        ],
    )
    def test_edge_cases_preserve_consecutive_underscores(self, snake, camel):
        assert _to_camel_case(snake) == camel

    def test_empty_string(self):
        assert _to_camel_case("") == ""

    @pytest.mark.parametrize("word", ["word", "single"])
    def test_single_word_returns_unchanged(self, word):
        assert _to_camel_case(word) == word


class TestToSnakeCase:
    @pytest.mark.parametrize(
        "camel, snake",
        [
            ("camelCase", "camel_case"),
            ("fooBar", "foo_bar"),
            ("simpleField", "simple_field"),
            ("already_snake", "already_snake"),
            ("lowercase", "lowercase"),
        ],
    )
    def test_standard_cases(self, camel, snake):
        assert _to_snake_case(camel) == snake


class TestCamelizeKeys:
    def test_flat_dict(self):
        assert _camelize_keys({"foo_bar": 1, "baz_qux": 2}) == {
            "fooBar": 1,
            "bazQux": 2,
        }

    def test_nested_dict(self):
        assert _camelize_keys({"outer_field": {"inner_field": 42}}) == {
            "outerField": {"innerField": 42}
        }

    def test_list_of_dicts(self):
        assert _camelize_keys([{"foo_bar": 1}, {"baz_qux": 2}]) == [
            {"fooBar": 1},
            {"bazQux": 2},
        ]

    def test_scalars_unchanged(self):
        assert _camelize_keys(42) == 42
        assert _camelize_keys("foo_bar") == "foo_bar"
        assert _camelize_keys(None) is None


# ---------------------------------------------------------------------------
# BaseConfigModel — permissive base, no normalization
# ---------------------------------------------------------------------------


class TestBaseConfigModel:
    def test_extras_pass_through_unchanged_in_either_case(self):
        model = BaseConfigModel(extraField="x", another_extra="y")
        assert getattr(model, "extraField") == "x"
        assert model.another_extra == "y"

    def test_dump_emits_extras_unchanged(self):
        model = BaseConfigModel(camelKey="a", snake_key="b")
        assert model.model_dump(by_alias=True) == {
            "camelKey": "a",
            "snake_key": "b",
        }


# ---------------------------------------------------------------------------
# SnakeCaseExtrasModel — snake_case normalization by default 
# is opt-in via transform_kwargs_casing_scope to enable passthrough
# ---------------------------------------------------------------------------


class TestSnakeCaseExtrasModel:
    def test_extras_pass_through_unchanged_with_flag_false(self):
        with transform_kwargs_casing_scope(False):
            model = SnakeCaseExtrasModel(extraField="x", anotherCamel=42)
        assert model.extraField == "x"
        assert model.anotherCamel == 42

    def test_dump_emits_extras_unchanged_with_flag_false(self):
        with transform_kwargs_casing_scope(False):
            model = SnakeCaseExtrasModel(extraField="x")
            dumped = model.model_dump(by_alias=True)
        assert dumped == {"extraField": "x"}

    def test_extras_normalized_camel_to_snake_by_default(self):
        model = SnakeCaseExtrasModel(extraField="x", anotherCamel=42)
        assert model.extra_field == "x"
        assert model.another_camel == 42

    def test_snake_extras_are_idempotent_by_default(self):
        model = SnakeCaseExtrasModel(already_snake="value")
        assert model.already_snake == "value"

    def test_dump_emits_normalized_snake_keys_by_default(self):
        model = SnakeCaseExtrasModel(extraField="x")
        assert model.model_dump(by_alias=True) == {"extra_field": "x"}

    def test_request_model_extras_normalized_at_dump_regardless_of_scope_when_built(self):
        # Simulates a request model built before HTTPTransport.request() opens
        # the scope: model_post_init sees the explicit False passed at
        # construction, but the dump-time hook re-checks the policy active
        # when .model_dump() runs.
        with transform_kwargs_casing_scope(False):
            model = SnakeCaseExtrasModel(extraCamelKwarg="foo")
        assert model.extraCamelKwarg == "foo"

        with transform_kwargs_casing_scope(True):
            dumped = model.model_dump(by_alias=True)
        assert dumped == {"extra_camel_kwarg": "foo"}

        # Outside any scope, the ambient default (True) still normalizes.
        assert model.model_dump(by_alias=True) == {"extra_camel_kwarg": "foo"}


# ---------------------------------------------------------------------------
# CamelCaseDumpModel — recursive camelize on dump (by_alias only)
# ---------------------------------------------------------------------------


class TestCamelCaseDumpModel:
    def test_extras_pass_through_unchanged_with_flag_false(self):
        with transform_kwargs_casing_scope(False):
            model = CamelCaseDumpModel(snake_extra="value", another_snake=42)
            dumped = model.model_dump(by_alias=True)
        assert dumped == {
            "snake_extra": "value",
            "another_snake": 42,
        }

    def test_extras_emit_as_camel_by_default(self):
        model = CamelCaseDumpModel(snake_extra="value", another_snake=42)
        dumped = model.model_dump(by_alias=True)
        assert dumped == {
            "snakeExtra": "value",
            "anotherSnake": 42,
        }

    def test_extras_kept_as_snake_when_by_alias_false(self):
        # Mirrors the previous Numbers override: conversion is gated on by_alias.
        model = CamelCaseDumpModel(snake_extra="value")
        dumped = model.model_dump(by_alias=False)
        assert dumped == {"snake_extra": "value"}

    def test_nested_dict_fields_kept_raw_with_flag_false(self):
        class Outer(CamelCaseDumpModel):
            sms_configuration: Optional[Dict[str, Any]] = Field(
                default=None, alias="smsConfiguration"
            )
            voice_configuration: Optional[Dict[str, Any]] = Field(
                default=None, alias="voiceConfiguration"
            )

        with transform_kwargs_casing_scope(False):
            model = Outer(
                sms_configuration={"service_plan_id": "X"},
                voice_configuration={"appId": "Y", "type": "RTC"},
            )
            dumped = model.model_dump(by_alias=True)
        assert dumped == {
            "smsConfiguration": {"service_plan_id": "X"},
            "voiceConfiguration": {"appId": "Y", "type": "RTC"},
        }

    def test_nested_dict_keys_camelized_recursively_when_default(self):
        class Outer(CamelCaseDumpModel):
            sms_configuration: Optional[Dict[str, Any]] = Field(
                default=None, alias="smsConfiguration"
            )
            voice_configuration: Optional[Dict[str, Any]] = Field(
                default=None, alias="voiceConfiguration"
            )

        model = Outer(
                sms_configuration={"service_plan_id": "X"},
                voice_configuration={"appId": "Y", "type": "RTC"},
            )
        dumped = model.model_dump(by_alias=True)
        assert dumped == {
            "smsConfiguration": {"servicePlanId": "X"},
            "voiceConfiguration": {"appId": "Y", "type": "RTC"},
        }

    def test_model_dump_json_also_camelizes_when_default_enabled(self):
        model = CamelCaseDumpModel(snake_extra="value")
        dumped = model.model_dump_json(by_alias=True)
        assert json.loads(dumped) == {
            "snakeExtra": "value",
        }


# ---------------------------------------------------------------------------
# Composition — each model handles its own extras independently
# ---------------------------------------------------------------------------


class TestComposition:
    def test_nested_snake_extras_models_keep_extras_raw_with_flag_false(self):
        class Inner(SnakeCaseExtrasModel):
            foo_bar: int

        class Outer(SnakeCaseExtrasModel):
            inner: Inner
            name: int

        with transform_kwargs_casing_scope(False):
            outer = Outer(
                inner={"foo_bar": 12, "extraField": 123},
                name=112,
                extraAtRoot="extra",
            )
        assert outer.inner.foo_bar == 12
        assert outer.inner.extraField == 123
        assert outer.extraAtRoot == "extra"

    def test_nested_snake_extras_models_normalize_at_every_level_when_default(self):
        class Inner(SnakeCaseExtrasModel):
            foo_bar: int

        class Outer(SnakeCaseExtrasModel):
            inner: Inner
            name: int

        outer = Outer(
                inner={"foo_bar": 12, "extraField": 123},
                name=112,
                extraAtRoot="extra",
            )
        assert outer.inner.foo_bar == 12
        assert outer.inner.extra_field == 123
        assert outer.extra_at_root == "extra"

    def test_snake_extras_inner_in_base_config_outer_keeps_outer_extras_raw(self):
        class Common(SnakeCaseExtrasModel):
            foo_bar: int

        class Outer(BaseConfigModel):
            common: Common
            name: int

        outer = Outer(
                common={"foo_bar": 12, "extraField": 123},
                name=112,
                extraAtRoot="extra",
            )
        assert outer.common.extra_field == 123
        assert getattr(outer, "extraAtRoot") == "extra"

    def test_camel_dump_outer_keeps_nested_free_form_dict_keys_raw_with_flag_false(self):
        class Outer(CamelCaseDumpModel):
            payload: Dict[str, Any]

        with transform_kwargs_casing_scope(False):
            outer = Outer(payload={"user_id": "abc", "nested_obj": {"item_id": 1}})
            dumped = outer.model_dump(by_alias=True)
        assert dumped == {
            "payload": {"user_id": "abc", "nested_obj": {"item_id": 1}}
        }

    def test_camel_dump_outer_camelizes_nested_free_form_dict_keys_when_default(self):
        class Outer(CamelCaseDumpModel):
            payload: Dict[str, Any]

        with transform_kwargs_casing_scope(True):
            outer = Outer(payload={"user_id": "abc", "nested_obj": {"item_id": 1}})
            dumped = outer.model_dump(by_alias=True)
        assert dumped == {
            "payload": {"userId": "abc", "nestedObj": {"itemId": 1}}
        }
