import redis
import os
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

def create_connection():
    r = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        password=os.getenv('REDIS_PASSWORD'),
        decode_responses=True
    )
    return r