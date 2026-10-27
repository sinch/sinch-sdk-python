import pytest
from sinch.core.clients.transport_settings import TransportSettings


class TestTransportSettings:
    def test_defaults(self):
        settings = TransportSettings()

        assert settings.timeout_seconds == 60
        assert settings.use_sinch_auth is True

    def test_accepts_a_custom_timeout(self):
        assert TransportSettings(timeout_seconds=30).timeout_seconds == 30

    def test_allows_zero_timeout(self):
        assert TransportSettings(timeout_seconds=0).timeout_seconds == 0

    def test_rejects_negative_timeout(self):
        with pytest.raises(ValueError, match="timeout_seconds must be zero or greater, got: -1"):
            TransportSettings(timeout_seconds=-1)

    def test_accepts_a_float_timeout(self):
        assert TransportSettings(timeout_seconds=2.5).timeout_seconds == 2.5

    @pytest.mark.parametrize("timeout_seconds", [None, "60", float("inf"), float("nan")])
    def test_rejects_non_finite_number_timeout(self, timeout_seconds):
        with pytest.raises(ValueError, match="timeout_seconds must be a finite number"):
            TransportSettings(timeout_seconds=timeout_seconds)

    def test_accepts_disabling_sinch_auth(self):
        assert TransportSettings(use_sinch_auth=False).use_sinch_auth is False

    @pytest.mark.parametrize("use_sinch_auth", [None, 0, "false"])
    def test_rejects_non_boolean_use_sinch_auth(self, use_sinch_auth):
        with pytest.raises(ValueError, match="use_sinch_auth must be a boolean"):
            TransportSettings(use_sinch_auth=use_sinch_auth)
