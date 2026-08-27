from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from orders_service.application.dto import CreateOrderInput, CreateOrderItemInput
from orders_service.application.exceptions import OrderNotFoundApplicationError
from orders_service.application.use_cases.create_order import CreateOrderUseCase
from orders_service.application.use_cases.delete_order import DeleteOrderUseCase
from orders_service.application.use_cases.get_order import GetOrderUseCase
from orders_service.application.use_cases.list_orders import ListOrdersUseCase
from orders_service.application.use_cases.update_order_status import (
    UpdateOrderStatusUseCase,
)
from orders_service.domain.exceptions import DomainError
from orders_service.infrastructure.db.repositories import SqlAlchemyOrderRepository
from orders_service.infrastructure.notifications.logging_notifier import (
    LoggingOrderNotifier,
)
from orders_service.presentation.dependencies import (
    get_current_user,
    get_order_notifier,
    get_order_repository,
)
from orders_service.presentation.schemas.orders import (
    OrderCreateRequest,
    OrderResponse,
    OrderStatusUpdateRequest,
)

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    data: OrderCreateRequest,
    repository: SqlAlchemyOrderRepository = Depends(get_order_repository),
    notifier: LoggingOrderNotifier = Depends(get_order_notifier),
) -> OrderResponse:
    try:
        result = CreateOrderUseCase(repository, notifier).execute(
            CreateOrderInput(
                customer_email=str(data.customer_email),
                items=[
                    CreateOrderItemInput(
                        product_name=item.product_name,
                        quantity=item.quantity,
                        unit_price=item.unit_price,
                    )
                    for item in data.items
                ],
            )
        )
        return OrderResponse.model_validate(result)
    except DomainError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error


@router.get("", response_model=list[OrderResponse])
def list_orders(
    repository: SqlAlchemyOrderRepository = Depends(get_order_repository),
) -> list[OrderResponse]:
    result = ListOrdersUseCase(repository).execute()
    return [OrderResponse.model_validate(order) for order in result]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: UUID,
    repository: SqlAlchemyOrderRepository = Depends(get_order_repository),
) -> OrderResponse:
    try:
        result = GetOrderUseCase(repository).execute(order_id)
        return OrderResponse.model_validate(result)
    except OrderNotFoundApplicationError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: UUID,
    data: OrderStatusUpdateRequest,
    repository: SqlAlchemyOrderRepository = Depends(get_order_repository),
) -> OrderResponse:
    try:
        result = UpdateOrderStatusUseCase(repository).execute(
            order_id,
            data.status,
        )
        return OrderResponse.model_validate(result)
    except OrderNotFoundApplicationError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except DomainError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: UUID,
    repository: SqlAlchemyOrderRepository = Depends(get_order_repository),
) -> Response:
    try:
        DeleteOrderUseCase(repository).execute(order_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except OrderNotFoundApplicationError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
