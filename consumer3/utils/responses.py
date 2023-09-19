from configs.clog import LOGGER
from typing import Union

def gen_response(msg:str, data: dict = None, success:bool = False) -> dict:
    # print('Message', msg)
    LOGGER.info(msg)
    return {'message': msg, 'data': data, 'success': success}
