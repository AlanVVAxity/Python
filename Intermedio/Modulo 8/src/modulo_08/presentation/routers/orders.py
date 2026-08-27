from fastapi import APIRouter, Depends, HTTPException, status

from modulo_08.application.dto import CreateOrderInput
from modulo_08.application.exceptions import NotificationError
from modulo_08.application.use_cases.create_order import CreateOrderUseCase
from modulo_08.domain.exceptions import InvalidOrderError
from modulo_08.presentation.dependencies import get_create_order_use_case
from modulo_08.presentation.schemas import CreateOrderRequest, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    request: CreateOrderRequest,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
) -> OrderResponse:
    try:
        result = use_case.execute(
            CreateOrderInput(
                customer_email=request.customer_email,
                product_name=request.product_name,
                quantity=request.quantity,
                unit_price=request.unit_price,
            )
        )
    except InvalidOrderError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
    except NotificationError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    return OrderResponse.model_validate(result)
