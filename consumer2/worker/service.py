from aiokafka import (
    # KafkaConsumer,
    TopicPartition,
    ConsumerRecord
)
from configs.clog import LOGGER
import asyncio
from .utils import ( getConfluentConsumer )
from typing import (
    Callable,
    Dict, List,
)
from parse import *



def consume_general(topic: str, callback: Callable):
    consumer = getConfluentConsumer()
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # LOGGER.info("No message found!")
                continue

            if msg.error():
                LOGGER.error(msg.error())
                continue
            # else:
            topic, key, value = parse(msg)
            callback(topic, key, value)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def parse_message(topic: str, key: str, value: str):
    LOGGER.info(f"Consumed message with topic={topic}, key={key}, value={value}")

def confluent_consume_mytopic():
    c = getConfluentConsumer()
    topic: str = 'my_topic'
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

        LOGGER.info('RECV MSG: {}'.format(msg.value().decode('utf-8')))

    c.close()

def confluent_consume(topic: str = 'my_topic'):
    c = getConfluentConsumer()
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

        LOGGER.info('RECV MSG: {}'.format(msg.value().decode('utf-8')))

    c.close()

async def consume_all():
    # confluent_consume()
    # confluent_consume_mytopic()
    consume_general('my_topic', parse_message)
    pass