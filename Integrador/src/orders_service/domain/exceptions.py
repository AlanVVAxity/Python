class DomainError(Exception):
    pass


class InvalidOrderStatusError(DomainError):
    pass


class InvalidOrderItemError(DomainError):
    pass


class OrderNotFoundError(DomainError):
    pass
