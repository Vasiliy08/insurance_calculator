import datetime
from dataclasses import dataclass

import orjson
from aiokafka.producer import AIOKafkaProducer


@dataclass
class KafkaMessageBroker:
    producer: AIOKafkaProducer

    async def log(self, message, user, action):
        batch = self.producer.create_batch()
        dct = {
            "message": message,
            "user": user,
            "action": action,
            "timestamp": datetime.datetime.now(),
        }
        value = orjson.dumps(dct)
        batch.append(key=None, value=value, timestamp=None)
        # partitions = await self.producer.partitions_for('my_topic')
        await self.producer.send_batch(batch, topic="my_topic", partition=0)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()
