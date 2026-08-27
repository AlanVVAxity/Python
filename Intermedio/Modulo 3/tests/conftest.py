from collections.abc import Callable
from decimal import Decimal

import pytest

from modulo_03.order import OrderItem


@pytest.fixture
def create_item() -> Callable[[str, Decimal, int], OrderItem]:
    def _create_item(
        product_name: str = "Producto de prueba",
        unit_price: Decimal = Decimal("10.00"),
        quantity: int = 1,
    ) -> OrderItem:
        return OrderItem(
            product_name=product_name,
            unit_price=unit_price,
            quantity=quantity,
        )

    return _create_item
