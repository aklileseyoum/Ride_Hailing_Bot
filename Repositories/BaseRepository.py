import redis
import json


class BaseRepository:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def get(self, key):
        value = self.redis.get(key)
        return json.loads(value)

    def set(self, key, value):
        return self.redis.set(key, json.dumps(value))

    def delete(self, key):
        self.redis.delete(key)

    def exists(self, key):
        return self.redis.exists(key)

    def expire(self, key, seconds):
        self.redis.expire(key, seconds)

    def ttl(self, key):
        return self.redis.ttl(key)

    def keys(self, pattern):
        return self.redis.keys(pattern)

    def flush(self):
        self.redis.flushdb()

    def flush_all(self):
        self.redis.flushall()
