from sinch.domains.number_lookup.models.v1.shared import SimSwap


def test_sim_swap_valid_expects_parsed_data():
    """Test a valid instance of SimSwap"""
    data = {
        "swapped": True,
        "swapPeriod": "SP24H",
    }
    sim_swap = SimSwap(**data)

    assert sim_swap.swapped is True
    assert sim_swap.swap_period == "SP24H"


def test_sim_swap_error_expects_parsed_data():
    """Test a valid instance of SimSwap with error"""
    data = {
        "error": {
            "status": 100,
            "title": "Feature Disabled",
            "detail": "SimSwap feature is currently disabled.",
        }
    }
    sim_swap = SimSwap(**data)

    assert sim_swap.error.status == 100
    assert sim_swap.error.title == "Feature Disabled"
    assert sim_swap.error.detail == "SimSwap feature is currently disabled."


def test_sim_swap_optional_fields_expects_parsed_data():
    """Test missing optional fields in SimSwap"""
    data = {}
    sim_swap = SimSwap(**data)

    assert sim_swap.swapped is None
    assert sim_swap.swap_period is None
