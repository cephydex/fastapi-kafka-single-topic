from fastapi import APIRouter, Form, File, Request, status, UploadFile, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
import json
from typing import Union
import httpx
from utils.libs import get_httpx_client
from helpers import (divide_chunks_comp, read_csv_file
        , read_csv_file_by_index, 
        generate_sms_destinations, generate_sms_payload
    )
from serializer import BytesEncoder
from configs.csets import settings
from configs.clog import logging


router = APIRouter(
    prefix="/ui",
    tags=["ui"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
LOGGER = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/sendsms", response_class=HTMLResponse)
def send_sms(request: Request):
    return templates.TemplateResponse("send.html", context={"request": request})

@router.post("/sendsms", response_class=RedirectResponse)
# def validate_sms(request: Request, message: str = Form(...), customer_file: UploadFile  = File(...),):
# async def validate_sms(request: Request, message: list = Form(...), customer_file: Union[UploadFile, None] = None, client: httpx.AsyncClient = Depends(get_httpx_client)):
async def validate_sms(request: Request, customer_file: Union[UploadFile, None] = None, client: httpx.AsyncClient = Depends(get_httpx_client)):
    form_data = await request.form()

    suffix = "csv"    
    is_csv_file = customer_file.filename.lower().endswith(suffix)
    valid_file_type = customer_file != None and not is_csv_file
    if valid_file_type:
        resp_data = {
            "success": False,
            "rtype": "danger",
            "message": "Sorry! invalid file uploaded, check and retry"
        }
        return templates.TemplateResponse("success.html", context={"request": resp_data})

    # validate key column name
    column_key = form_data["field_name"]
    opts = ['phone_number', 'phone number', 'phonenumber', 'phone_no', 'phone no', 'phoneno' ,'phonenum', 'phone_num', 'phone num']
    arr_set = set(opts)
    if form_data["field_name"] != '' and column_key not in arr_set:
        column_key = None
        resp_data = {
            "success": False,
            "rtype": "danger",
            "message": 'Oops! you did not specify the "phone number" column name'
        }
        return templates.TemplateResponse("success.html", context={"request": resp_data})
   

    # validate for file not empty and message
    valid_credentials = customer_file != None and form_data["message"] != ''
    URL = settings.wg_url
    if valid_credentials:
        # read csv file and return key phone nos
        # phone_list = read_csv_file(customer_file, key='phone_number')
        phone_nums = settings.test_phone_nums
        if form_data["field_name"] == '':
            phone_list = read_csv_file_by_index(customer_file)
        else:        
            phone_list = read_csv_file_by_index(customer_file, key = column_key)

        # print("Phone list", column_key, phone_list)
        # exit()

        chunks_comp = divide_chunks_comp(phone_list, 200)
        LOGGER.info(f'Chuncks size: {len(chunks_comp)}')

        # loop and send messages
        for item in chunks_comp:
            LOGGER.info(f'Chuncks content size: {len(item)}')
            # destinations list
            destinations = generate_sms_destinations(item)
            if settings.test_mode:
                LOGGER.warn('Test mode: ' + str(settings.test_mode))
                destinations = generate_sms_destinations(phone_nums, 1)

            # msg = message.encode('utf-8')
            msg = form_data["message"].encode('ascii')
            payload = generate_sms_payload(msg, destinations)
            
            headers={'Content-Type': 'application/json'}
            try:
                response = await client.post(URL, data=json.dumps(payload, cls=BytesEncoder), headers=headers)
                json_response = response.json()
                LOGGER.info('SMS Response')
                LOGGER.info(json_response)
                chk_str = json_response['status'].lower()
                
                if json_response and chk_str != 'accepted':
                    LOGGER.warn(chk_str)
                    break
            
            except Exception as ex:
                LOGGER.error(ex)
            
            if settings.test_mode:
                LOGGER.warn(f'Break step: {settings.test_mode}')
                break

        resp_data = {
            "success": True,
            "rtype": "success",
            "message": "File uploaded for processing, please wait..."
        }
        return templates.TemplateResponse("success.html", context={"request": resp_data})
    
    redirect_url = request.url_for('send_sms')+ '?x-error=Invalid+credentials'
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND, headers={"x-error": "Invalid credentials"})

