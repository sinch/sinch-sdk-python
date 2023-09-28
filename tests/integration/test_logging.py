import logging
import tempfile
from unittest.mock import Mock


def mock_http_transport(client):
    client.configuration.transport.session = Mock()
    client.configuration.transport.session.request.return_value.content = {}
    client.configuration.transport.session.request.return_value.headers = {}
    client.configuration.transport.prepare_request = Mock()
    client.configuration.transport.authenticate = Mock()
    return client


def test_default_logger(sinch_client_sync, caplog):
    sinch_client_sync.configuration.logger.setLevel(logging.DEBUG)
    sinch_client = mock_http_transport(sinch_client_sync)
    http_endpoint = Mock()
    sinch_client.configuration.transport.request(http_endpoint)
    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == "DEBUG"


def test_changing_logger_name_within_the_client(sinch_client_sync, caplog):
    sinch_client_sync.configuration.logger.setLevel(logging.DEBUG)
    sinch_client_sync.configuration.logger.name = "SumOlimpijczyk"
    sinch_client = mock_http_transport(sinch_client_sync)
    http_endpoint = Mock()
    sinch_client.configuration.transport.request(http_endpoint)
    assert len(caplog.records) == 2
    assert caplog.records[0].name == "SumOlimpijczyk"


def test_logger_with_logging_to_file(sinch_client_sync):
    with tempfile.NamedTemporaryFile() as fp:
        file_handler = logging.FileHandler(fp.name)
        sinch_client_sync.configuration.logger.setLevel(logging.DEBUG)
        sinch_client_sync.configuration.logger.addHandler(file_handler)
        sinch_client = mock_http_transport(sinch_client_sync)
        http_endpoint = Mock()
        sinch_client.configuration.transport.request(http_endpoint)
        logging_output = fp.read().decode("utf-8")
        assert "HTTP" in logging_output
        assert "response" in logging_output
