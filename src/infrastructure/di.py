from functools import lru_cache

from punq import Container, Scope

from src.infrastructure.repository import RateRepository


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(RateRepository, scope=Scope.singleton)
    return container
