from examples.logging_example import main, sinch_client


def test_sinch_client_logging_with_e2e_test(
    caplog,
    auth_origin,
    numbers_origin
):
    sinch_client.configuration.auth_origin = auth_origin
    sinch_client.configuration.numbers_origin = numbers_origin
    sinch_client.configuration.disable_https = True
    main()

    assert len(caplog.records)

    with open("/tmp/test_python_logging.log") as fd:
        log_messages = fd.read()
        assert "DEBUG" in log_messages
        assert "myapp.sinch" in log_messages
