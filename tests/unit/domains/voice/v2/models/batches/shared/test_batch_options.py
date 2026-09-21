from sinch.domains.voice.models.v2.batches.shared.batch_options import (
    BatchOptions,
)


def test_batch_options_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = BatchOptions(max_cps=5, ttl_seconds=90)

    assert model.max_cps == 5
    assert model.ttl_seconds == 90

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {"maxCps": 5, "ttlSeconds": 90}


def test_batch_options_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = BatchOptions()

    assert model.max_cps is None
    assert model.ttl_seconds is None
