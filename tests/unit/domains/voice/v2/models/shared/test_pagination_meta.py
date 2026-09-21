from sinch.domains.voice.models.v2.shared.pagination_meta import (
    PaginationMeta,
)


def test_pagination_meta_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = PaginationMeta(total_count=100, page_count=5)

    assert model.total_count == 100
    assert model.page_count == 5

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["totalCount"] == 100
    assert alias_dump["pageCount"] == 5
