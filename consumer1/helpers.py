# import asyncio
# import httpx
import csv, codecs
from fastapi import UploadFile, HTTPException
from configs.csets import settings
from typing import Union


'''
Generate destination numbers for WIGAL batch message request
'''
def generate_sms_destinations(num_list, dcount: int = 0):
    destinations = []
    dest_cnt = (dcount, len(num_list)) [dcount == 0]
    # print('value check for destination', dest_cnt)

    for i in range(dest_cnt):
        if not (i > len(num_list) -1):
            destinations.append({
                    "destination": num_list[i],
                    "msgid": 101
                })

    return destinations


'''
Generate message payload for WIGAL batch message request
'''
def generate_sms_payload(msg: str, destinations: list):
    payload = {
        "username": settings.wg_username,
        "password": settings.wg_password,
        "senderid": settings.wg_senderid,
        "destinations": destinations,
        "message": msg,
        "service": "SMS",
        "subject": "Broadcast",
        # "fromemail": "email@email.com",
        "smstype": "text",
    }

    return payload

'''
Get header column from CSV file
'''
def get_headers(csvReader_list):
    # csv_reader = csv.DictReader(csv_file)
    # csvReader = csv.DictReader(codecs.iterdecode(uploaded_file.file, 'utf-8'))
    # dict_from_csv = dict(list(csvReader)[0])
    dict_from_csv = dict(csvReader_list[0])
    # get list from the dict
    column_list = list(dict_from_csv.keys())

    return column_list

'''
Traverse CSV file and return value of the specified key
'''
def read_csv_file(uploaded_file: UploadFile, key: str):
    # CSV reader instance
    csvReader = csv.DictReader(codecs.iterdecode(uploaded_file.file, 'utf-8'))
    
    phone_list = []
    for rows in csvReader:             
        phone_number = rows[key]
        phone_list.append(phone_number)
    uploaded_file.file.close() #close file

    return phone_list


def get_key_index(header_list: list, key: str):
    header_list =  [x.lower() for x in header_list]
    # indexes = [i for i, x in enumerate(xs) if x == 'foo'] # all indexes    
    kIndex = -1
    try:
        return header_list.index(key)
    except Exception:    
        return kIndex


'''
Traverse CSV file and return value of the specified key
'''
def read_csv_file_by_index(uploaded_file: UploadFile, key: Union[str, None] = 'phone_number'):
    # CSV reader instance
    csvReader_list = list( csv.DictReader(codecs.iterdecode(uploaded_file.file, 'utf-8')) )
    header_list_raw = get_headers(csvReader_list)

    kIndex = get_key_index(header_list_raw, key)
    if kIndex < 0:
        raise HTTPException(500, "Invalid file operation: key 'phone_number' not found")
    phone_list = []
    mKey = header_list_raw[kIndex]

    for rows in csvReader_list:
        # value may come as float; convert to int
        if rows[mKey] != '':
            phone_number: int = int(float(rows[mKey]))
            phone_list.append(phone_number)

    uploaded_file.file.close() #close file
    return phone_list


'''
Traverse CSV file and return value of the specified key
'''
def read_csv_file_by_index_singlekey(uploaded_file: UploadFile, key: str):
    # CSV reader instance
    csvReader_list = list( csv.DictReader(codecs.iterdecode(uploaded_file.file, 'utf-8')) )
    header_list_raw = get_headers(csvReader_list)

    kIndex = get_key_index(header_list_raw, key)
    if kIndex < 0:
        raise HTTPException(500, "Invalid file operation: key 'phone_number' not found")
    phone_list = []
    mKey = header_list_raw[kIndex]
    print('selector detail', kIndex, mKey, )
    
    csvReader2 = csv.reader(uploaded_file.file)
    print('csv reader', csvReader2)
    for rows in csvReader_list:
        # value may come as float; convert to int
        if rows[mKey] != '':
            phone_number: int = int(float(rows[mKey]))
            # print('val', str(phone_number))
            phone_list.append(phone_number)
    uploaded_file.file.close() #close file

    return phone_list

'''
Divide large array (list) into smaller chunks for easy handling
'''
def divide_chunks(l, n):      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]


def divide_chunks_comp(l, n): 
    # using list comprehension 
    chunk = [l[i:i + n] for i in range(0, len(l), n)]
    return chunk # this must be passed to a list