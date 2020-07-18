import pytest

from model import Batch, OrderLine, allocate, OutOfStock
from test_batches import tomorrow, today, later


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "SPOON", 100, eta=today)
    medium = Batch("normal-batch", "SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "SPOON", 100, eta=later)
    line = OrderLine("order1", "SPOON", 10)

    allocate(line, [medium, latest, earliest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
    line = OrderLine("order1", "HIGHBROW-POSTER", 10)

    ref = allocate(line, [in_stock_batch, shipment_batch])

    assert ref == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch-ref", "SPOON", 100, eta=today)
    line = OrderLine("order1", "SPOON", 100)

    allocate(line, [batch])

    with pytest.raises(OutOfStock, match="SPOON"):
        line2 = OrderLine("order2", "SPOON", 10)
        allocate(line2, [batch])

