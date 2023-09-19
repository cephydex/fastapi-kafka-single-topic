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
from confluent_kafka import Consumer


def confluent_consume_mytopic():
    c = Consumer({
        # 'bootstrap.servers': 'mybroker',
        'bootstrap.servers': kafka_instance,
        'group.id': 'my_group',
        'auto.offset.reset': 'earliest'
    })
    topic: str = 'my_topic2'
    LOGGER.info('Consumer subscription: BEFORE')
    c.subscribe([topic])
    LOGGER.info('Consumer subscribed to: {}'.format(topic))

    while True:
        msg = c.poll(1.0)
        if msg is None:
            LOGGER.info("No message found for now")
            continue
        if msg.error():
            # print("Consumer error: {}".format(msg.error()))
            LOGGER.info("Consumer error: {}".format(msg.error()))
            continue

        # print('RECV MSG: {}'.format(msg.value().decode('utf-8')))
        LOGGER.info('RECV MSG: {}'.format(msg.value().decode('utf-8')))

    c.close()

def confluent_consume(topic: str = 'my_topic'):
    c = Consumer({
        # 'bootstrap.servers': 'mybroker',
        'bootstrap.servers': kafka_instance,
        # 'group.id': 'my_group2',
        'auto.offset.reset': 'earliest'
    })
    # topic: str = 'my_topic'
    c.subscribe([topic])
    LOGGER.info('Consumer subscribed to: {}'.format(topic))

    while True:
        msg = c.poll(1.0)
        if msg is None:
            LOGGER.info("No message found for now")
            continue
        if msg.error():
            LOGGER.info("Consumer error: {}".format(msg.error()))
            continue

        # print('RECV MSG: {}'.format(msg.value().decode('utf-8')))
        LOGGER.info('RECV MSG: {}'.format(msg.value().decode('utf-8')))

    c.close()


async def get_messages_from_my_topic():
    # consumer = AIOKafkaConsumer(
    #     'my_topic', 'my_other_topic',
    #     bootstrap_servers='localhost:9092',
    #     group_id="my-group")
    # Get cluster layout and join group `my-group`
    consumer = get_consumer("my_topic")
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            # print("CONS MY_TOPIC: ", msg.topic, msg.partition, msg.offset,
            #       msg.key, msg.value, msg.timestamp)
            LOGGER.info("CONS MY_TOPIC:")
            LOGGER.info(msg)
    finally:
        await consumer.stop()


# async def consume_by_topic(topic: str):
#     consumer = get_consumer(topic)
#     await consumer.start()
#     # consumer.
#     try:
#         # Consume messages
#         async for msg in consumer:
#             # print("consumed: ", msg.topic, msg.partition, msg.offset,
#             #       msg.key, msg.value, msg.timestamp)
#             LOGGER.info("MY_TOPIC2:")
#             LOGGER.info(msg)
#     finally:
#         await consumer.stop()


async def consume_by_topic_unend(topic: str):
    """
    Listens to real-time broker/message topic.
    """
    while True:
        try:
            consumer = get_consumer(topic)
            await consumer.start()
            partition: TopicPartition = list(consumer.assinment())[0]
            await consumer.seek_to_end(partition)

            while True:
                response: Dict[TopicPartition, List[ConsumerRecord]] = \
                            await consumer.getmany(partition, timeout_ms=1000)
                if partition in response:
                    for record in response[partition]:
                        LOGGER.info('RECORD DET')
                        LOGGER.info(record)
                        pass
                        # output.put_nowait(self.order_book_class.diff_message_from_kafka(record))

        except asyncio.CancelledError:
            raise
        except Exception:
                LOGGER.error("Unknown error. Retrying after 5 seconds.", exc_info=True)
                await asyncio.sleep(5.0)
        finally:
            await consumer.stop()


async def consume_by_topic_unend_simple(topic: str):
    while True:
        try:
            consumer = get_consumer(topic)
            await consumer.start()
            # Consume messages
            async for msg in consumer:
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                    msg.key, msg.value, msg.timestamp)
                LOGGER.info(msg)
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
    await get_messages_from_my_topic()
    # await consume_by_topic("my_topic")

    await consume_by_topic("my_topic2")

    # confluent_consume('my_topic2')
    # confluent_consume_mytopic()
    asyncio.create_task( confluent_consume('my_topic2') )
    asyncio.create_task( confluent_consume_mytopic() )

    # await consume_by_topic_unend("my_topic")
    # await consume_by_topic_unend_simple("my_topic")
    # await consume_by_topic_unend(topic: str)
    # asyncio.create_task(consume())
    pass