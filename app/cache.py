import redis
import json
import os


REDIS_URL = os.getenv("REDIS_URL")
r = redis.from_url(REDIS_URL, decode_responses=True)


def get_cache(key):
    data = r.get(key)
    if data:
        print("CACHE HIT")
        return json.loads(data)
    print("CACHE MISS")
    return None


def set_cache(key, value, ttl=60):
    r.setex(key, ttl, json.dumps(value))