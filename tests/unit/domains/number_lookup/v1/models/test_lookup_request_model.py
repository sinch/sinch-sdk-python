from sinch.domains.number_lookup.models.v1.internal import LookupNumberRequest


def test_lookup_number_request_minimal_expects_valid_request():
    """Test minimal lookup request with only number."""
    request = LookupNumberRequest(number="+15551234567")
    assert request.number == "+15551234567"
    assert request.features is None
    assert request.rnd_feature_options is None


def test_lookup_number_request_with_features_expects_valid_request():
    """Test lookup request with features."""
    request = LookupNumberRequest(
        number="+15552345678", features=["LineType", "SimSwap"]
    )
    assert request.number == "+15552345678"
    assert request.features == ["LineType", "SimSwap"]


def test_lookup_number_request_with_rnd_options_expects_valid_request():
    """Test lookup request with RND feature options."""
    request = LookupNumberRequest(
        number="+15553456789",
        features=["RND"],
        rnd_feature_options={"contact_date": "2025-01-01"},
    )
    assert request.number == "+15553456789"
    assert request.features == ["RND"]
    assert request.rnd_feature_options == {"contact_date": "2025-01-01"}


def test_lookup_number_request_model_dump_expects_camel_case():
    """Test that model dump converts to camelCase."""
    request = LookupNumberRequest(
        number="+15554567890",
        features=["LineType"],
        rnd_feature_options={"contact_date": "2025-01-01"},
    )
    dumped = request.model_dump(by_alias=True)
    assert "number" in dumped
    assert "features" in dumped
    assert "rndFeatureOptions" in dumped
    assert "rnd_feature_options" not in dumped


def test_lookup_number_request_all_features_expects_valid_request():
    """Test lookup request with all available features."""
    request = LookupNumberRequest(
        number="+15555678901",
        features=["LineType", "SimSwap", "VoIPDetection", "RND"],
    )
    assert len(request.features) == 4
    assert "LineType" in request.features
    assert "SimSwap" in request.features
    assert "VoIPDetection" in request.features
    assert "RND" in request.features
