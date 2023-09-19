from .utils import get_producer
import json
# import asyncio

async def send_test_one(msg: str, topic: str = 'my_topic'):
   prod = get_producer()
   await prod.start()
   try:
      # Produce message
      # await prod.send_and_wait("my_topic", b"Super message")
      # await prod.send_and_wait("my_topic", json.dumps(msg,default=lambda x:x.dict()).encode("ascii"))
      await prod.send_and_wait(topic, json.dumps(msg,default=lambda x:x.dict()).encode("ascii"))
      # await prod.send_and_wait("my_topic", json.dumps(msg,default=lambda x:x.dict()).encode("ascii"))
   finally:
      await prod.stop() # Wait for pending messages to be delivered or expire.

async def send_with_key(msg, key:str, topic: str = 'my_topic'):
   prod = get_producer()
   await prod.start()
   try:
      # Produce message
      await prod.send_and_wait(topic, value=json.dumps(msg,default=lambda x:x.dict()).encode("ascii"))
      # await prod.send_and_wait(topic, key=key, value=json.dumps(msg,default=lambda x:x.dict()).encode("ascii"))
   finally:
      await prod.stop() # Wait for pending messages to be delivered or expire.


def serialize(data):
   return bytes(json.dumps(data), "utf-8")