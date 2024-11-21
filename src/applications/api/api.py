from datetime import date
from typing import Annotated

import orjson
import punq
from fastapi import APIRouter, Depends, File, HTTPException, Path, Query, UploadFile, status

from src.applications.api.schemas import (
    ApiResponse,
    Block,
    ErrorSchema,
    ListPaginatedResponse,
    PaginationIn,
    PaginationOut,
)
from src.exceptions.base import ApplicationException
from src.infrastructure.di import init_container
from src.infrastructure.kafka import KafkaMessageBroker
from src.infrastructure.repository import RateRepository

router = APIRouter(tags=[""])


@router.post(
    "/upload-rates/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт для создания и обновления json файла",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def upload_rates(
    file: Annotated[UploadFile, File()],
    container: Annotated[punq.Container, Depends(init_container)],
):
    contents = await file.read()
    rates_data = orjson.loads(contents)
    container_rate: RateRepository = container.resolve(RateRepository)
    try:
        old_rate = await container_rate.update_rates_in_db(rates_data)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    print("old_rate", old_rate)
    container_kafka: KafkaMessageBroker = container.resolve(KafkaMessageBroker)
    for rate, value in old_rate.items():
        await container_kafka.log(
            message=f"Для груза {rate.cargo_type} на дату {rate.effective_date} обновленна ставка. Старая ставка {rate.rate}. Новая ставка {value}",
            user="admin",
            action="Обновление",
        )

    return {"message": "Данные успешно обновлены"}


@router.get(
    "/calculate/",
    status_code=status.HTTP_200_OK,
    description="Рассчитать стоимость страхования",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def calculate_insurance(
    cargo_type: str,
    declared_value: float,
    container: Annotated[punq.Container, Depends(init_container)],
    date: date = Query(description="yyyy-mm-dd"),
):
    container: RateRepository = container.resolve(RateRepository)
    try:
        result = await container.calculate_insurance(cargo_type, declared_value, date)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return {"Стоимость": result}


@router.get(
    "/rates/",
    response_model=ApiResponse[ListPaginatedResponse[Block]],
    status_code=status.HTTP_200_OK,
    description="Получить список всех ставок",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_all_rates(
    pagination: Annotated[PaginationIn, Query()],
    container: Annotated[punq.Container, Depends(init_container)],
):
    container: RateRepository = container.resolve(RateRepository)

    rates = await container.get_all_rates(pagination)
    count = await container.get_count_rate()

    return ApiResponse(
        data=ListPaginatedResponse(
            items=rates,
            pagination=PaginationOut(
                page=pagination.offset,
                limit=pagination.limit,
                total=count,
                order_by=pagination.order_by,
            ),
        )
    )


@router.delete(
    "/rates/{cargo_type}/{effective_date}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить тариф",
)
async def delete_rate(
    cargo_type: str,
    container: Annotated[punq.Container, Depends(init_container)],
    effective_date: date = Path(description="yyyy-mm-dd"),
):
    container_rate: RateRepository = container.resolve(RateRepository)
    try:
        await container_rate.delete_rate(cargo_type, effective_date)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    container_kafka: KafkaMessageBroker = container.resolve(KafkaMessageBroker)
    await container_kafka.log(
        message=f"Груз {cargo_type} на дату {effective_date} удалён",
        user="admin",
        action="Удаление",
    )


@router.patch(
    "/rates/{cargo_type}/{effective_date}/",
    status_code=status.HTTP_200_OK,
    description="Редактировать тариф",
)
async def edit_rate(
    cargo_type: str,
    new_rate_value: float,
    container: Annotated[punq.Container, Depends(init_container)],
    effective_date: date = Path(description="yyyy-mm-dd"),
):
    container_rate: RateRepository = container.resolve(RateRepository)
    try:
        old_rate = await container_rate.edit_rate(cargo_type, effective_date, new_rate_value)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    container_kafka: KafkaMessageBroker = container.resolve(KafkaMessageBroker)
    await container_kafka.log(
        message=f"Для груза {cargo_type} на дату {effective_date} обновленна ставка. Старая ставка {old_rate}. Новая ставка {new_rate_value}",
        user="admin",
        action="Обновление",
    )

    return {"message": "Тариф успешно обновлен"}
