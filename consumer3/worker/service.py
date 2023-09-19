from aiokafka import (
    # KafkaConsumer,
    TopicPartition,
    ConsumerRecord
)
from configs.clog import LOGGER
import asyncio
from .utils import get_consumer, get_consumer_nolp, kafka_instance
from typing import (
    Dict, List
)


async def consume_by_topic(topic: str):
    consumer = get_consumer(topic)
    await consumer.start()
    # consumer.
    try:
        # Consume messages
        async for msg in consumer:
            LOGGER.info("CN3 MSG:")
            LOGGER.info(msg)
    finally:
        await consumer.stop()


async def consume_by_topic_unend_simple(topic: str):
    while True:
        try:
            consumer = get_consumer(topic)
            await consumer.start()
            # Consume messages
            async for msg in consumer:
                LOGGER.info("RECV CON3: {} | {} | {}".format(msg.topic, msg.key, msg.value))
                # LOGGER.info(msg)
        except asyncio.CancelledError:
            raise
        except Exception:
                LOGGER.error("Unknown error. Retrying after 5 seconds.", exc_info=True)
                await asyncio.sleep(5.0)


async def consumer_simple(topic: str):
        loop = asyncio.get_event_loop()
        consumer = get_consumer_nolp(topic, loop)
        await consumer.start()
        
        try:
            # total_msgs = 0
            while True:
                async for msg in consumer:
                    LOGGER.info("MESSAGE")
                    LOGGER.info( msg)

        except asyncio.CancelledError:
            pass
        finally:
            await consumer.stop()

async def consume_all():
    # await consume_by_topic_unend("my_topic")
    await consume_by_topic_unend_simple("my_topic")
    # asyncio.create_task(consume())
    pass