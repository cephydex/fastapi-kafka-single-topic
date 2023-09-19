from fastapi import APIRouter, Response, Depends
from fastapi import status, Request
from server.app_logger import logger
from .schema import MessageRequest
from .service import send_test_one, send_with_key
from .utils import get_today
import asyncio


router = APIRouter(
            prefix='/api/v1/notty',
            tags=['Note'],
            responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {"message": "Request failed"}}
         )


@router.post("/send_one")
async def send_one(req_data: MessageRequest, response: Response,):
   print('req_data', req_data)
   resp_data = {
      'today': get_today(),
      'req_message': req_data.message
   }

   # loop = asyncio.get_event_loop()
   # loop.run_until_complete(send_test_one(req_data.message))
   await send_test_one(req_data.message, req_data.topic)
   logger.info("Queue message sent")
   logger.info(resp_data)
   return {
      'message': 'Test queue message sent successfully',
      'data': resp_data,
      'success': True
   }

import random
key_list = ["bulk_message", "player_win", "player_stake", "agent_stake"]
# rand_idx = random.randrange(len(key_list))

@router.post("/send_random")
# async def send_one(response: Response, token:str=Depends(JWTBearer())):
async def send_one(req_data: MessageRequest, response: Response,):   
   # random_key = key_list[rand_idx]
   random_key = random.choice(("bulk_message", "player_win", "player_stake", "agent_stake"))
   # random.choice(('xxx', 'yyy', 'zzz'))

   print('req_data', req_data)
   resp_data = {
      'today': get_today(),
      'req_message': req_data.message,
      'mkey': random_key,
   }

   # loop = asyncio.get_event_loop()
   # loop.run_until_complete(send_test_one(req_data.message))
   # await send_with_key(req_data.message, random_key, req_data.topic)
   await send_with_key(resp_data, random_key, req_data.topic)
   logger.info("Queue message sent with key")
   logger.info(resp_data)
   return {
      'message': 'Test queue message sent successfully',
      'data': resp_data,
      'success': True
   }
   

