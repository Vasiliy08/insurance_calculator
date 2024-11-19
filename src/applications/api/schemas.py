from datetime import date
from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field

TData = TypeVar("TData")
TListItem = TypeVar("TListItem")


class ErrorSchema(BaseModel):
    error: str


class Block(BaseModel):
    cargo_type: str
    rate: float | int
    effective_date: date


class PaginationIn(BaseModel):
    offset: int = 0
    limit: int = 5
    order_by: Literal["asc", "desc"] = "asc"


class PaginationOut(BaseModel):
    page: int
    limit: int
    total: int
    order_by: Literal["asc", "desc"]


class ListPaginatedResponse(BaseModel, Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOut


class ApiResponse(BaseModel, Generic[TData]):
    data: TData | dict = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)
