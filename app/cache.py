import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def get_cache(key):
    data = r.get(key)
    if data:
        print("CACHE HIT")
        return json.loads(data)
    print("CACHE MISS")
    return None


def set_cache(key, value, ttl=60):
    r.setex(key, ttl, json.dumps(value))