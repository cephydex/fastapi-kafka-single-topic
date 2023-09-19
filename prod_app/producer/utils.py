import calendar
from datetime import date
from config.settings import settings
from aiokafka import AIOKafkaProducer
import asyncio

# kafka_instance=os.getenv('KAFKA_INSTANCE')
kafka_instance= settings.KAFKA_INSTANCE

def get_today(shorten: bool = True) -> str:
    d = date.today()
    # get day name (eng)
    day_name = calendar.day_name[d.weekday()]
    day_name = day_name.lower()
    
    return {True: day_name[0:3], False: day_name } [ shorten ]

def get_producer():
   loop = asyncio.get_event_loop()
   #  producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
   producer = AIOKafkaProducer(loop=loop, bootstrap_servers=kafka_instance)
   return producer

