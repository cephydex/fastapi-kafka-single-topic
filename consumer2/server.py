from fastapi import FastAPI
from worker.router import router as worker_router
from configs.csets import settings
from configs.clog import LOGGER
from worker.service import consume_all
import asyncio

app = FastAPI()
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

