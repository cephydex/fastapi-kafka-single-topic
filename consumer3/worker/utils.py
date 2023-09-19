from aiokafka import AIOKafkaConsumer
from configs.csets import settings
import asyncio

kafka_instance= settings.KAFKA_INSTANCE

def get_consumer(topic: str):
   ev_loop = asyncio.get_event_loop()
   consumer = AIOKafkaConsumer(topic, 
                                loop=ev_loop, 
                                bootstrap_servers=kafka_instance,
                                group_id="mega_main1", 
                                auto_offset_reset="earliest",
                                enable_auto_commit=False,
                           )
   return consumer

def get_consumer_nolp(topic: str, loop: asyncio.AbstractEventLoop):
   consumer = AIOKafkaConsumer(topic, 
                                loop=loop, 
                                bootstrap_servers=kafka_instance,
                                # group_id="test_group", 
                                auto_offset_reset="earliest",
                                enable_auto_commit=False,
                           )
   return consumer