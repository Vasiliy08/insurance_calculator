from contextlib import asynccontextmanager

import punq
from fastapi import FastAPI

from src.applications.router import main_router
from src.infrastructure.di import init_container
from src.infrastructure.kafka import KafkaMessageBroker


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: punq.Container = init_container()
    producer: KafkaMessageBroker = container.resolve(KafkaMessageBroker)
    await producer.start()

    yield

    await producer.stop()


def web_app_factory() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/api/docs",
    )
    app.include_router(main_router)
    return app
