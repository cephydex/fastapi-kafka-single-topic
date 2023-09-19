from fastapi import FastAPI
# from functools import lru_cache
import logging
import requests
import json
from serializer import BytesEncoder
from ui import frontend
from worker.router import router as worker_router
from helpers import generate_sms_destinations, generate_sms_payload
from configs.csets import settings
from configs.clog import LOGGER
from worker.service import consume_all
import asyncio

app = FastAPI()
app.include_router(frontend.router)
app.include_router(worker_router)

@app.get("/")
async def root():
    return {"server": "I'm alive"}

@app.get('/ping')
def index_request():
    return {"message": "pong"}

@app.get('/health_check')
def index_request():
    return {
        "message": "healthy"
    }

URL = settings.wg_url
phone_nums = settings.test_phone_nums

@app.get('/push_multiple')
async def multiple_request(num: int):
    destinations = generate_sms_destinations(phone_nums, num)
    json_destinations = json.dumps(destinations)
    # print(json_destinations)
    LOGGER.info(json_destinations)

    msg = 'Sorry to bother you, this is a test broadcast message. After reading this throw your phone away'
    msg = msg.encode('utf-8')
    payload = generate_sms_payload(msg, destinations)
    
    try:
        headers={'Content-Type': 'application/json'}
        response = requests.post(URL, data=json.dumps(payload, cls=BytesEncoder), headers=headers)
        json_response = response.json()
        # print(json_response)
        LOGGER.info(json_response)
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Messages sent",
                "result": json_response,
            }
        
    except Exception as ex:
        LOGGER.error(ex)
        return {
            "success": False,
            "message": str(ex),
        }
    
    return {
        "success": False,
        "message": "Messages could not be sent",
    }

@app.on_event("startup")
async def startup_event():
    try:
        await consume_all()
        LOGGER.info('App Events started successful')
        pass
    except Exception as e:
        # print('App Events startup error', str(e))
        LOGGER.info('App Events startup error')
        LOGGER.info(str(e))


@app.on_event("shutdown")
async def shutdown_event():
    try:
        # unsubscribe
        LOGGER.info('App Events shutdown successful')
        pass
    except Exception as e:
        # print('App Events shutdown error', str(e))
        ev_loop = asyncio.get_event_loop()
        ev_loop.stop()
        ev_loop.close()
        LOGGER.info('App Events shutdown error')
        LOGGER.info(str(e))

