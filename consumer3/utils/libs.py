from aiokafka import AIOKafkaConsumer
# from configs.csets import settings
from configs.csets import settings
import httpx
import asyncio


'''
Create httpx client for use in http requests
'''
async def httpx_async_client():
    # httpx.Client(http2=True)
    async with httpx.AsyncClient() as client:
        yield client

'''
Create httpx client for use in http requests
'''
async def get_httpx_client():
    # httpx.Client(http2=True)
    async with httpx.AsyncClient() as client:
        yield client
