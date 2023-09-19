from aiokafka import AIOKafkaConsumer
from configs.csets import settings
import asyncio
from confluent_kafka import Consumer

kafka_instance= settings.KAFKA_INSTANCE


def getConfluentConsumer():
    # c = Consumer({
    #     # 'bootstrap.servers': 'mybroker',
    #     'bootstrap.servers': kafka_instance,
    #     'group.id': 'my_group',
    #     'auto.offset.reset': 'earliest'
    # })
    return Consumer({
        'bootstrap.servers': kafka_instance,
        'group.id': 'mega_main',
        'auto.offset.reset': 'earliest'
    })
