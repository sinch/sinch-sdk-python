from sinch.domains.conversation.models.v1.sinch_events.inbound.payment_status_update_event import (
    PaymentStatusUpdateEvent,
)


def test_payment_status_update_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = PaymentStatusUpdateEvent(
        reference_id="order-1",
        payment_status="PAYMENT_STATUS_CAPTURED",
        payment_transaction_status="PAYMENT_STATUS_TRANSACTION_SUCCESS",
        payment_transaction_id="transaction-1",
    )

    assert model.reference_id == "order-1"
    assert model.payment_status == "PAYMENT_STATUS_CAPTURED"
    assert model.payment_transaction_status == "PAYMENT_STATUS_TRANSACTION_SUCCESS"
    assert model.payment_transaction_id == "transaction-1"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["reference_id"] == "order-1"
    assert alias_dump["payment_status"] == "PAYMENT_STATUS_CAPTURED"
    assert (
        alias_dump["payment_transaction_status"]
        == "PAYMENT_STATUS_TRANSACTION_SUCCESS"
    )
    assert alias_dump["payment_transaction_id"] == "transaction-1"


def test_payment_status_update_event_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = PaymentStatusUpdateEvent()

    assert model.reference_id is None
    assert model.payment_status is None
    assert model.payment_transaction_status is None
    assert model.payment_transaction_id is None
