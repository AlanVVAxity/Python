from functools import lru_cache

from modulo_08.application.use_cases.create_order import CreateOrderUseCase
from modulo_08.infrastructure.config import get_settings
from modulo_08.infrastructure.wiring.container import Container


@lru_cache
def get_container() -> Container:
    return Container(settings=get_settings())


def get_create_order_use_case() -> CreateOrderUseCase:
    return get_container().create_order_use_case()
