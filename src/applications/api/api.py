from datetime import date
from typing import Annotated

import orjson
import punq
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

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
    container: RateRepository = container.resolve(RateRepository)
    try:
        await container.update_rates_in_db(rates_data)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
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
