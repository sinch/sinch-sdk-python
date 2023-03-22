import pytest
from sinch.domains.sms.models.batches.responses import SendSMSBatchResponse


@pytest.mark.skip()
def test_send_sms_zen_of_python(sinch_client_sync, phone_number, origin_phone_number):
    zen = """
    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    """

    for line in zen.split("\n"):
        send_sms_response = sinch_client_sync.sms.batches.send(
            to=[phone_number],
            from_=origin_phone_number,
            body=line,
            feedback_enabled=True
        )

        assert isinstance(send_sms_response, SendSMSBatchResponse)


async def test_send_sms_async(sinch_client_async, phone_number, origin_phone_number):
    send_sms_response = await sinch_client_async.sms.batches.send(
        delivery_report="summary",
        to=[phone_number],
        from_=origin_phone_number,
        body="Asynchronous Spanish Inquisition",
        feedback_enabled=True,
    )
    assert isinstance(send_sms_response, SendSMSBatchResponse)


def test_send_sms_sync(sinch_client_sync, phone_number, origin_phone_number):
    send_sms_response = sinch_client_sync.sms.batches.send(
        delivery_report="summary",
        to=[phone_number],
        from_=origin_phone_number,
        body="Synchronous Spanish Inquisition",
        feedback_enabled=True,
    )
    assert isinstance(send_sms_response, SendSMSBatchResponse)
