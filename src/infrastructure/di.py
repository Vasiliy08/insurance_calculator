from functools import lru_cache

from aiokafka import AIOKafkaProducer
from punq import Container, Scope

from src.core.config import settings
from src.infrastructure.kafka import KafkaMessageBroker
from src.infrastructure.repository import RateRepository


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(RateRepository, scope=Scope.singleton)

    def create_message_broker():
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.kafka.KAFKA_URL),
        )

    container.register(KafkaMessageBroker, factory=create_message_broker, scope=Scope.singleton)

    return container
