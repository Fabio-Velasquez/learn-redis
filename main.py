import redis
import requests
from dotenv import load_dotenv
import os

# load .env variables 
load_dotenv()

# DFW box bound
# -97.5198145439,32.5434630462,-96.4816065361,33.22961999
WEST=-97.5198145439
SOUTH=32.5434630462
EAST=-96.4816065361
NORTH=33.22961999


def enrich_redis_geohash(restaurants_in_dfw, redis_connection):
    pipe = redis_connection.pipeline()
    count = 0
    for node in restaurants_in_dfw['elements']:
        lat = node.get('lat','lat_not_available')
        lon = node.get('lon','long_not_available')
        name = node.get('tags','tags_not_available').get('name','name_not_available')
        pipe.geoadd('restaurant', [lon, lat, name])
        count += 1

    results = pipe.execute()
    print(f"Pipeline results: {results}")
    print(f"Loaded {count} restaurants")

def main():
    redis_connection = create_connection()
    restaurants_in_dfw = fetch_restaurants(SOUTH,WEST,NORTH,EAST)
    print(f"Total elements found: {len(restaurants_in_dfw['elements'])}")
    print(f"First element sample: {restaurants_in_dfw['elements'][0]}")
    enrich_redis_geohash(restaurants_in_dfw, redis_connection)
    redis_connection.close()

def create_connection():
    r = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
     )
    return r
def fetch_restaurants(south, west, north, east):
    query = f"""
    [out:json];
    node["amenity"="restaurant"]({south},{west},{north},{east});
    out;
    """
    response = requests.post('https://overpass-api.de/api/interpreter', data=query)
    print(f"Status code: {response.status_code}")
    return response.json()

if __name__ == "__main__":
    main()