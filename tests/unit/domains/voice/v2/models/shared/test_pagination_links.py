from sinch.domains.voice.models.v2.shared.pagination_links import (
    PaginationLinks,
)


def test_pagination_links_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = PaginationLinks(
        first="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=20",
        last="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=5&pageSize=20",
        next="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=3&pageSize=20",
        prev="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=20",
        self_="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=20",
    )

    assert model.first == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=20"
    )
    assert model.last == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=5&pageSize=20"
    )
    assert model.next == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=3&pageSize=20"
    )
    assert model.prev == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=20"
    )
    assert model.self_ == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=20"
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["self"] == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=20"
    )


def test_pagination_links_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = PaginationLinks(
        first="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=20",
        last="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=5&pageSize=20",
        self_="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=20",
    )

    assert model.next is None
    assert model.prev is None
