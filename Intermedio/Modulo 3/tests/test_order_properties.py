from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from modulo_03.order import OrderItem


@pytest.mark.property
@given(
    unit_price=st.decimals(
        min_value=Decimal("0.01"),
        max_value=Decimal("10000.00"),
        places=2,
    ),
    quantity=st.integers(min_value=1, max_value=1000),
)
def test_item_subtotal_is_price_multiplied_by_quantity(
    unit_price: Decimal,
    quantity: int,
) -> None:
    item = OrderItem(
        product_name="Producto generado",
        unit_price=unit_price,
        quantity=quantity,
    )

    assert item.subtotal == unit_price * quantity
