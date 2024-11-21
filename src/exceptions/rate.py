from dataclasses import dataclass
from datetime import date

from src.exceptions.base import ApplicationException


@dataclass
class RateNotFoundException(ApplicationException):
    cargo_type: str
    date: date

    @property
    def message(self):
        return f"Нет соответствующей ставки для груза {self.cargo_type} на дату {self.date}"


@dataclass
class InvalidDateException(ApplicationException):
    date: date

    @property
    def message(self):
        return f"Неверный формат даты в json файле {self.date}, необходимый формат yyyy-mm-dd"
