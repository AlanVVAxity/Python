from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from modulo_02.repositories.order_repository import OrderRepository
from modulo_02.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from modulo_02.services.order_service import OrderNotFoundError, OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

repository = OrderRepository()
service = OrderService(repository)


def get_order_service() -> OrderService:
    return service


OrderServiceDependency = Annotated[OrderService, Depends(get_order_service)]


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una orden",
)
async def create_order(
    order_data: OrderCreate,
    order_service: OrderServiceDependency,
) -> OrderResponse:
    return order_service.create_order(order_data)


@router.get(
    "",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar órdenes",
)
async def list_orders(
    order_service: OrderServiceDependency,
) -> list[OrderResponse]:
    return order_service.list_orders()


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar una orden por identificador",
)
async def get_order(
    order_id: UUID,
    order_service: OrderServiceDependency,
) -> OrderResponse:
    try:
        return order_service.get_order(order_id)
    except OrderNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        ) from error


@router.put(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar una orden",
)
async def update_order(
    order_id: UUID,
    order_data: OrderUpdate,
    order_service: OrderServiceDependency,
) -> OrderResponse:
    try:
        return order_service.update_order(order_id, order_data)
    except OrderNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        ) from error


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una orden",
)
async def delete_order(
    order_id: UUID,
    order_service: OrderServiceDependency,
) -> Response:
    try:
        order_service.delete_order(order_id)
    except OrderNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        ) from error

    return Response(status_code=status.HTTP_204_NO_CONTENT)