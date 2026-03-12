import redis
import request
from dotenv import load_dotenv
import os
# load .env variables 
load_dotenv()



def main():
    r = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        password=os.getenv("REDIS_PASSWORD")
    )