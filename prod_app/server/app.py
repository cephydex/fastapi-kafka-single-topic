
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from server.app_logger import logger
from fastapi.staticfiles import StaticFiles
from producer.router import router as producer_router

app = FastAPI(
    title="Kafka Service",
    description="Webservice for Kafka producer",
    version="1.0.0",
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(producer_router)

@app.get("/", tags=["Root"])
async def root():
    logger.info("logging from the root logger")
    return {"message": 'Server connected successfully'}

@app.on_event("startup")
async def startup_event():
    try:
        # init all GraphqlClient subscription
        # loop.create_task(subscribe())

        # init all kafka producers
        # await produce(aioproducer,loop)
        pass
    except Exception as e:
          print('App Events startup error', str(e))


@app.on_event("shutdown")
async def shutdown_event():
    try:
        # stop all kafka producers
        # await unproduce(aioproducer,loop)
        pass
    except Exception as e:
        print('App Events shutdown error', str(e))

