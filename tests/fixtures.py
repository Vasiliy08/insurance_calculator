import punq

from src.infrastructure.di import init_container
from src.infrastructure.repository import RateRepository


def mock_test_container() -> punq.Container:
    container = init_container()

    container.register(RateRepository)

    return container
